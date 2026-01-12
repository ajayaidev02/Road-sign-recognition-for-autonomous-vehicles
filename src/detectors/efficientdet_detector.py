from typing import List
from ..config import DetectorConfig
from ..utils.types import Detection
from .base import Detector


class EfficientDetDetector(Detector):
    def __init__(self, cfg: DetectorConfig) -> None:
        self.cfg = cfg
        # Placeholder for actual EfficientDet initialization
        self.model = None

    def detect(self, frame) -> List[Detection]:
        if self.model is None:
            h, w, _ = frame.shape
            return [Detection(label="efficientdet_stub", confidence=0.18, bbox=(w // 3, h // 3, w // 2, h // 2))]
        # Implement EfficientDet inference here
        return []
