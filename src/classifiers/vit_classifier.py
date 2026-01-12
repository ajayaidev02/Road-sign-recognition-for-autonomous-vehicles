from typing import Optional
import numpy as np

try:
    import torch
    from torchvision import models, transforms
except ImportError:  # pragma: no cover - optional
    torch = None
    models = None
    transforms = None

from ..config import ClassifierConfig
from ..utils.types import ClassificationResult, Detection


class ViTClassifier:
    def __init__(self, cfg: ClassifierConfig) -> None:
        self.cfg = cfg
        self.device = cfg.device
        self.model = None
        self.preprocess = None
        if torch and models:
            self.model = models.vit_b_16(weights=models.ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1)
            if cfg.model_path:
                state = torch.load(cfg.model_path, map_location=cfg.device)
                self.model.load_state_dict(state)
            self.model.eval().to(cfg.device)
            weights = models.ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1
            self.preprocess = weights.transforms()
        else:
            print("Torch/torchvision missing; ViT classifier will emit stubs.")

    def classify(self, frame: np.ndarray, detections: list[Detection]) -> Optional[ClassificationResult]:
        if not detections:
            return None
        x1, y1, x2, y2 = detections[0].bbox
        crop = frame[y1:y2, x1:x2]
        if self.model is None or self.preprocess is None or torch is None:
            return ClassificationResult(label="unclassified", confidence=0.1, logits=None)

        with torch.no_grad():
            tensor = self.preprocess(crop).unsqueeze(0).to(self.device)
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=1)
            conf, idx = torch.max(probs, dim=1)
            label = self.cfg.class_names[idx.item()] if self.cfg.class_names else str(idx.item())
            return ClassificationResult(label=label, confidence=float(conf.item()), logits=logits.cpu().numpy())
