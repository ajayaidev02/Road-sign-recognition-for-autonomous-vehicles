import argparse
from typing import Optional

from .config import AppConfig
from .pipeline import process_stream
from .ui.dashboard import Dashboard
from .utils.video_source import open_stream


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Road sign recognition console app for Indian roads")
    parser.add_argument("--source", default="0", help="Camera index or video file path")
    parser.add_argument("--resize", nargs=2, type=int, metavar=("W", "H"), help="Optional resize")
    parser.add_argument("--detector", default=None, help="Detector name (yolov8n, yolov9c, efficientdet_d0, ssd_mobilenet_v3)")
    parser.add_argument("--classifier", default=None, help="Classifier name (resnet50, efficientnet_b4, mobilenet_v3_large, vit_b_16)")
    parser.add_argument("--max-frames", type=int, default=None, help="Stop after N frames")
    parser.add_argument("--no-preview", action="store_true", help="Disable preview rendering (TUI only)")
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
    return cfg


def main():
    args = parse_args()
    cfg = build_config(args)
    dashboard = Dashboard()
    frames = open_stream(cfg.runtime.source, cfg.runtime.resize)

    def limited_frames():
        try:
            for idx, frame in frames:
                if cfg.runtime.max_frames and idx >= cfg.runtime.max_frames:
                    break
                yield idx, frame
        finally:
            pass  # frame cleanup happens in open_stream context

    try:
        result_stream = process_stream(limited_frames(), cfg)
        dashboard.run_live(result_stream)
    except KeyboardInterrupt:
        print("\nShutdown complete.")
    except Exception as e:
        print(f"Fatal error: {e}")
        raise
    finally:
        print("Application closed.")


if __name__ == "__main__":
    main()
