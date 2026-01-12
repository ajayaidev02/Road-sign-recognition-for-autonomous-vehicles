from typing import List
try:
    from ultralytics import YOLO  # type: ignore
except ImportError:  # pragma: no cover - optional dep
    YOLO = None

from ..config import DetectorConfig
from ..utils.types import Detection
from .base import Detector


class YoloDetector(Detector):
    def __init__(self, cfg: DetectorConfig) -> None:
        self.cfg = cfg
        self.model = None
        if YOLO:
            model_name = cfg.model_path or cfg.name
            self.model = YOLO(model_name)
        else:
            print("YOLO not installed; detector will emit stubs.")

    def detect(self, frame) -> List[Detection]:
        if not self.model:
            h, w, _ = frame.shape
            return [Detection(label="unknown", confidence=0.2, bbox=(w // 4, h // 4, w // 2, h // 2))]

        results = self.model.predict(frame, imgsz=640, conf=self.cfg.conf_threshold, iou=self.cfg.iou_threshold, device=self.cfg.device, half=self.cfg.half_precision, max_det=self.cfg.max_det, verbose=False)
        detections: List[Detection] = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int).tolist()
                conf = float(box.conf[0].cpu().item())
                cls_id = int(box.cls[0].item())
                label = self.model.model.names.get(cls_id, str(cls_id)) if hasattr(self.model, "model") else str(cls_id)
                detections.append(Detection(label=label, confidence=conf, bbox=(x1, y1, x2, y2)))
        return detections
