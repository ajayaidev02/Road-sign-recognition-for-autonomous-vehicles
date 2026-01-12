import time
from collections import deque
from typing import Deque, Optional


class ThroughputMeter:
    def __init__(self, window: int = 30) -> None:
        self.window = window
        self.times: Deque[float] = deque(maxlen=window)
        self.last_time: Optional[float] = None

    def tick(self) -> float:
        now = time.perf_counter()
        if self.last_time is None:
            self.last_time = now
            return 0.0
        delta = now - self.last_time
        self.last_time = now
        self.times.append(delta)
        if not self.times:
            return 0.0
        avg = sum(self.times) / len(self.times)
        return 1.0 / avg if avg > 0 else 0.0
