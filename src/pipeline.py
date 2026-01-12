import time
from typing import Generator, Iterable

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
from .utils.types import FrameResult
from .utils.safety import SafetyGuard


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


def process_stream(frames: Iterable[tuple[int, any]], cfg: AppConfig) -> Generator[FrameResult, None, None]:
    detector = build_detector(cfg)
    classifier = build_classifier(cfg)
    llm = LLMExplainer(cfg.llm)
    safety = SafetyGuard(cfg.safety)
    meter = ThroughputMeter()

    for frame_id, frame in frames:
        start = time.perf_counter()
        fps = meter.tick()
        detections = detector.detect(frame)
        classification = classifier.classify(frame, detections)
        llm_text = None
        if classification:
            llm_text = llm.explain(classification.label, classification.confidence)
        latency_ms = (time.perf_counter() - start) * 1000
        safety_state = safety.evaluate(fps, detections[0] if detections else None, classification)
        yield FrameResult(
            detections=detections,
            classification=classification,
            llm_explanation=llm_text,
            frame_id=frame_id,
            fps=fps,
            latency_ms=latency_ms,
            degraded=safety_state.degraded,
        )
