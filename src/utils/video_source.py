import cv2
from typing import Generator, Optional, Union


def open_stream(source: Union[str, int], resize: Optional[tuple[int, int]] = None) -> Generator[tuple[int, any], None, None]:
    cap = cv2.VideoCapture(int(source) if str(source).isdigit() else source)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video source: {source}")
    frame_id = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if resize:
                frame = cv2.resize(frame, resize)
            yield frame_id, frame
            frame_id += 1
    finally:
        cap.release()
