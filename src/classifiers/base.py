from abc import ABC, abstractmethod
from typing import Optional
from ..utils.types import ClassificationResult


class Classifier(ABC):
    @abstractmethod
    def classify(self, frame, detections) -> Optional[ClassificationResult]:
        raise NotImplementedError
