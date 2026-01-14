from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np


@dataclass
class Detection:
    label: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2
    track_id: Optional[int] = None


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
    safety_tier: str = "unknown"
    manual_override: bool = False
    stage_latency: Optional[Dict[str, float]] = None
