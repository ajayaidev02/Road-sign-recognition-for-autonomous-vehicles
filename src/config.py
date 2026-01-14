from dataclasses import dataclass, field
from typing import List, Optional, Tuple


def _get_device() -> str:
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


@dataclass
class DetectorConfig:
    name: str = "yolov8n"  # options: yolov8n, yolov9c, efficientdet_d0, ssd_mobilenet_v3
    conf_threshold: float = 0.35
    iou_threshold: float = 0.45
    device: str = field(default_factory=_get_device)  # auto-detect CUDA
    max_det: int = 10
    half_precision: bool = True
    model_path: Optional[str] = None  # custom weights for Indian datasets


@dataclass
class ClassifierConfig:
    name: str = "efficientnet_b4"  # options: resnet50, efficientnet_b4, mobilenet_v3_large, vit_b_16
    num_classes: int = 120
    device: str = field(default_factory=_get_device)  # auto-detect CUDA
    half_precision: bool = False
    model_path: Optional[str] = None
    class_names: List[str] = field(default_factory=list)


@dataclass
class LLMConfig:
    provider: str = "openai"  # or "huggingface"
    model: str = "gpt-4.1-mini"  # or local LLaMA/phi
    api_key_env: str = "LLM_API_KEY"
    max_tokens: int = 160
    temperature: float = 0.2
    safety_bias: float = 0.25  # increase safety tone


@dataclass
class SafetyConfig:
    alert_confidence: float = 0.4
    critical_confidence: float = 0.25
    fps_floor: float = 10.0
    allow_manual_override: bool = True
    stable_frames: int = 3  # frames required before LLM/ADAS actions
    risk_tier_high: float = 0.8
    risk_tier_med: float = 0.6
    risk_tier_warn: float = 0.4


@dataclass
class PreprocessConfig:
    enable_clahe: bool = True
    enable_blur: bool = True
    blur_kernel: int = 3
    enable_bilateral: bool = False
    enable_sharpen: bool = True
    enable_hsv_mask: bool = True
    enable_adaptive_thresh: bool = False
    enable_gamma: bool = False
    gamma: float = 1.2
    enable_dehaze: bool = False


@dataclass
class TrackingConfig:
    iou_threshold: float = 0.5
    max_age: int = 30
    min_stable: int = 3


@dataclass
class RuntimeConfig:
    source: str = "0"  # webcam id or video path
    resize: Optional[Tuple[int, int]] = None  # (width, height)
    show_preview: bool = False
    max_frames: Optional[int] = None
    target_fps: float = 20.0
    frame_queue: int = 5


@dataclass
class AppConfig:
    detector: DetectorConfig = field(default_factory=DetectorConfig)
    classifier: ClassifierConfig = field(default_factory=ClassifierConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)
    preprocess: PreprocessConfig = field(default_factory=PreprocessConfig)
    tracking: TrackingConfig = field(default_factory=TrackingConfig)
