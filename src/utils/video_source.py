import cv2
import threading
import time
from queue import Queue, Full, Empty
from typing import Generator, Optional, Union


class FrameStream:
    def __init__(self, source: Union[str, int], resize: Optional[tuple[int, int]] = None, max_queue: int = 5, target_fps: float = 20.0) -> None:
        self.source = source
        self.resize = resize
        self.max_queue = max_queue
        self.target_fps = target_fps
        self._queue: Queue = Queue(maxsize=max_queue)
        self._cap = None
        self._thread = None
        self._running = False
        self._frame_id = 0

    def start(self):
        self._cap = cv2.VideoCapture(int(self.source) if str(self.source).isdigit() else self.source)
        if not self._cap.isOpened():
            raise RuntimeError(f"Unable to open video source: {self.source}")
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        return self

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        if self._cap:
            self._cap.release()

    def _loop(self):
        min_interval = 1.0 / max(self.target_fps, 1e-3)
        while self._running and self._cap:
            start = time.perf_counter()
            ok, frame = self._cap.read()
            if not ok:
                self._running = False
                break
            if self.resize:
                frame = cv2.resize(frame, self.resize)
            item = (self._frame_id, frame)
            try:
                self._queue.put(item, timeout=0.01)
            except Full:
                # drop the oldest to maintain latency bounds
                try:
                    self._queue.get_nowait()
                except Empty:
                    pass
                self._queue.put(item, timeout=0.01)
            self._frame_id += 1
            elapsed = time.perf_counter() - start
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)

    def frames(self) -> Generator[tuple[int, any], None, None]:
        while self._running:
            try:
                yield self._queue.get(timeout=0.1)
            except Empty:
                if not self._running:
                    break


def open_stream(source: Union[str, int], resize: Optional[tuple[int, int]] = None) -> Generator[tuple[int, any], None, None]:
    stream = FrameStream(source, resize).start()
    try:
        for item in stream.frames():
            yield item
    finally:
        stream.stop()
