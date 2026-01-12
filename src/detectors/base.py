from abc import ABC, abstractmethod
from typing import List
from ..utils.types import Detection


class Detector(ABC):
    @abstractmethod
    def detect(self, frame) -> List[Detection]:
        raise NotImplementedError
