import argparse
from typing import Optional

from .config import AppConfig
from .pipeline import process_stream
from .ui.dashboard import Dashboard
from .utils.video_source import FrameStream
from .utils.controls import ControlListener, ControlState


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Road sign recognition console app for Indian roads")
    parser.add_argument("--source", default="0", help="Camera index or video file path")
    parser.add_argument("--resize", nargs=2, type=int, metavar=("W", "H"), help="Optional resize")
    parser.add_argument("--detector", default=None, help="Detector name (yolov8n, yolov9c, efficientdet_d0, ssd_mobilenet_v3)")
    parser.add_argument("--classifier", default=None, help="Classifier name (resnet50, efficientnet_b4, mobilenet_v3_large, vit_b_16)")
    parser.add_argument("--max-frames", type=int, default=None, help="Stop after N frames")
    parser.add_argument("--no-preview", action="store_true", help="Disable preview rendering (TUI only)")
    parser.add_argument("--target-fps", type=float, default=20.0, help="Target capture FPS with frame skipping")
    parser.add_argument("--queue", type=int, default=5, help="Frame queue size for capture thread")
    return parser.parse_args()


def build_config(args: argparse.Namespace) -> AppConfig:
    cfg = AppConfig()
    if args.detector:
        cfg.detector.name = args.detector
    if args.classifier:
        cfg.classifier.name = args.classifier
    if args.resize:
        cfg.runtime.resize = (args.resize[0], args.resize[1])
    cfg.runtime.source = args.source
    cfg.runtime.max_frames = args.max_frames
    cfg.runtime.show_preview = not args.no_preview
    cfg.runtime.target_fps = args.target_fps
    cfg.runtime.frame_queue = args.queue
    return cfg


def main():
    args = parse_args()
    cfg = build_config(args)
    dashboard = Dashboard()
    controls = ControlState()
    control_thread = ControlListener(controls)
    control_thread.start()
    stream = FrameStream(cfg.runtime.source, cfg.runtime.resize, max_queue=cfg.runtime.frame_queue, target_fps=cfg.runtime.target_fps).start()

    def limited_frames():
        try:
            for idx, frame in stream.frames():
                yield idx, frame
        finally:
            stream.stop()
            control_thread.stop()

    try:
        result_stream = process_stream(limited_frames(), cfg, controls)
        dashboard.run_live(result_stream)
    except KeyboardInterrupt:
        print("\nShutdown complete.")
    except Exception as e:
        print(f"Fatal error: {e}")
        raise
    finally:
        control_thread.stop()
        stream.stop()
        print("Application closed.")


if __name__ == "__main__":
    main()
