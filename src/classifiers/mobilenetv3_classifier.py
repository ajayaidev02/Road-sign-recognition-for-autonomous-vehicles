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


class MobileNetV3Classifier:
    def __init__(self, cfg: ClassifierConfig) -> None:
        self.cfg = cfg
        self.device = cfg.device
        self.model = None
        self.preprocess = None
        if torch and models:
            self.model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.IMAGENET1K_V2)
            if cfg.model_path:
                state = torch.load(cfg.model_path, map_location=cfg.device)
                self.model.load_state_dict(state)
            self.model.eval().to(cfg.device)
            self.preprocess = transforms.Compose([
                transforms.ToPILImage(),
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
        else:
            print("Torch/torchvision missing; MobileNetV3 classifier will emit stubs.")

    def classify(self, frame: np.ndarray, detections: list[Detection]) -> Optional[ClassificationResult]:
        if not detections:
            return None
        x1, y1, x2, y2 = detections[0].bbox
        crop = frame[y1:y2, x1:x2]
        if self.model is None or self.preprocess is None or torch is None:
            return ClassificationResult(label="unclassified", confidence=0.12, logits=None)

        with torch.no_grad():
            tensor = self.preprocess(crop).unsqueeze(0).to(self.device)
            if self.cfg.half_precision:
                tensor = tensor.half()
                self.model.half()
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=1)
            conf, idx = torch.max(probs, dim=1)
            label = self.cfg.class_names[idx.item()] if self.cfg.class_names else str(idx.item())
            return ClassificationResult(label=label, confidence=float(conf.item()), logits=logits.cpu().numpy())
