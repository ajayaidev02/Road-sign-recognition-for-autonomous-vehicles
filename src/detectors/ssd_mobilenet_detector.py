from typing import List
from ..config import DetectorConfig
from ..utils.types import Detection
from .base import Detector


class SSDMobileNetDetector(Detector):
    def __init__(self, cfg: DetectorConfig) -> None:
        self.cfg = cfg
        self.model = None  # Plug in a TensorFlow/ONNX implementation as needed

    def detect(self, frame) -> List[Detection]:
        if self.model is None:
            h, w, _ = frame.shape
            return [Detection(label="ssd_stub", confidence=0.15, bbox=(w // 5, h // 5, w // 2, h // 2))]
        return []
