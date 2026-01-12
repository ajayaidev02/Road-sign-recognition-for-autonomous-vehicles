from dataclasses import dataclass
from typing import List, Optional, Tuple
import numpy as np


@dataclass
class Detection:
    label: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2


@dataclass
class ClassificationResult:
    label: str
    confidence: float
    logits: Optional[np.ndarray] = None


@dataclass
class FrameResult:
    detections: List[Detection]
    classification: Optional[ClassificationResult]
    llm_explanation: Optional[str]
    frame_id: int
    fps: float
    latency_ms: float
    degraded: bool = False
