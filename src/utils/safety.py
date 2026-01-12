from dataclasses import dataclass
from typing import Optional
from ..config import SafetyConfig
from .types import Detection, ClassificationResult


@dataclass
class SafetyState:
    degraded: bool = False
    alert_message: Optional[str] = None
    manual_override: bool = False


class SafetyGuard:
    def __init__(self, cfg: SafetyConfig) -> None:
        self.cfg = cfg

    def evaluate(self, fps: float, detection: Optional[Detection], classification: Optional[ClassificationResult]) -> SafetyState:
        degraded = False
        alert: Optional[str] = None

        if fps and fps < self.cfg.fps_floor:
            degraded = True
            alert = f"Low FPS ({fps:.1f}) - entering graceful degradation"

        if detection and detection.confidence < self.cfg.critical_confidence:
            degraded = True
            alert = "Detection confidence critical - holding actions"
        elif detection and detection.confidence < self.cfg.alert_confidence:
            alert = "Low detection confidence"

        if classification and classification.confidence < self.cfg.critical_confidence:
            degraded = True
            alert = "Classification confidence critical"
        elif classification and classification.confidence < self.cfg.alert_confidence:
            alert = "Low classification confidence"

        return SafetyState(degraded=degraded, alert_message=alert, manual_override=self.cfg.allow_manual_override)
