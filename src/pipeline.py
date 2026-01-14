import time
from typing import Generator, Iterable, Optional

from .config import AppConfig
from .detectors.yolo_detector import YoloDetector
from .detectors.efficientdet_detector import EfficientDetDetector
from .detectors.ssd_mobilenet_detector import SSDMobileNetDetector
from .classifiers.resnet_classifier import ResNetClassifier
from .classifiers.efficientnet_classifier import EfficientNetClassifier
from .classifiers.mobilenetv3_classifier import MobileNetV3Classifier
from .classifiers.vit_classifier import ViTClassifier
from .llm.explainer import LLMExplainer
from .utils.metrics import ThroughputMeter
from .utils.types import ClassificationResult, Detection, FrameResult
from .utils.safety import SafetyGuard
from .utils.preprocess import preprocess_frame
from .utils.tracker import SimpleTracker
from .utils.controls import ControlState


def build_detector(cfg: AppConfig):
    name = cfg.detector.name.lower()
    if name.startswith("yolo"):
        return YoloDetector(cfg.detector)
    if name.startswith("efficientdet"):
        return EfficientDetDetector(cfg.detector)
    return SSDMobileNetDetector(cfg.detector)


def build_classifier(cfg: AppConfig):
    name = cfg.classifier.name.lower()
    if name.startswith("resnet"):
        return ResNetClassifier(cfg.classifier)
    if "efficientnet" in name:
        return EfficientNetClassifier(cfg.classifier)
    if "mobilenet" in name:
        return MobileNetV3Classifier(cfg.classifier)
    return ViTClassifier(cfg.classifier)


def _fuse(det: Optional[Detection], cls: Optional[ClassificationResult]) -> Optional[ClassificationResult]:
    if det is None and cls is None:
        return None
    if det is None:
        return cls
    if cls is None:
        return ClassificationResult(label=det.label, confidence=det.confidence, logits=None)
    if cls.confidence >= det.confidence:
        return ClassificationResult(label=cls.label, confidence=cls.confidence, logits=cls.logits)
    return ClassificationResult(label=det.label, confidence=det.confidence, logits=cls.logits)


def _safety_tier(conf: float, cfg: AppConfig) -> str:
    if conf >= cfg.safety.risk_tier_high:
        return "adas"
    if conf >= cfg.safety.risk_tier_med:
        return "safe"
    if conf >= cfg.safety.risk_tier_warn:
        return "warn"
    return "ignore"


def process_stream(frames: Iterable[tuple[int, any]], cfg: AppConfig, controls: Optional[ControlState] = None) -> Generator[FrameResult, None, None]:
    detector = build_detector(cfg)
    classifier = build_classifier(cfg)
    llm = LLMExplainer(cfg.llm)
    safety = SafetyGuard(cfg.safety)
    tracker = SimpleTracker(cfg.tracking.iou_threshold, cfg.tracking.max_age, cfg.tracking.min_stable)
    meter = ThroughputMeter()
    llm_cache = {}

    for frame_id, frame in frames:
        if controls and controls.request_quit:
            break
        if cfg.runtime.max_frames and frame_id >= cfg.runtime.max_frames:
            break
        if controls and controls.paused:
            time.sleep(0.05)
            continue

        stage_latency = {}
        loop_start = time.perf_counter()

        t0 = time.perf_counter()
        processed = preprocess_frame(frame, cfg.preprocess)
        stage_latency["preprocess_ms"] = (time.perf_counter() - t0) * 1000

        t1 = time.perf_counter()
        detections = detector.detect(processed)
        detections = [d for d in detections if d.confidence >= cfg.detector.conf_threshold]
        detections = tracker.update(detections)
        stage_latency["detect_ms"] = (time.perf_counter() - t1) * 1000

        primary_det = detections[0] if detections else None

        t2 = time.perf_counter()
        cls_result = classifier.classify(processed, detections) if detections else None
        stage_latency["classify_ms"] = (time.perf_counter() - t2) * 1000

        fused = _fuse(primary_det, cls_result)

        llm_text = None
        t3 = time.perf_counter()
        if fused and primary_det:
            stable = tracker.is_stable(primary_det.track_id)
            gate = fused.confidence >= 0.75 and stable
            cache_key = primary_det.track_id
            if gate and cache_key in llm_cache:
                llm_text = llm_cache[cache_key]
            elif gate and (not controls or not controls.manual_override):
                llm_text = llm.explain(fused.label, fused.confidence)
                if cache_key is not None:
                    llm_cache[cache_key] = llm_text
        stage_latency["llm_ms"] = (time.perf_counter() - t3) * 1000

        fps = meter.tick()
        latency_ms = (time.perf_counter() - loop_start) * 1000

        safety_state = safety.evaluate(fps, primary_det, fused, manual_override=bool(controls and controls.manual_override))
        tier = _safety_tier(fused.confidence if fused else 0.0, cfg)

        result = FrameResult(
            detections=detections,
            classification=fused,
            llm_explanation=llm_text,
            frame_id=frame_id,
            fps=fps,
            latency_ms=latency_ms,
            degraded=safety_state.degraded,
            safety_tier=tier,
            manual_override=bool(controls and controls.manual_override),
            stage_latency=stage_latency,
        )
        yield result
