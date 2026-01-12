# Road Sign Recognition for Autonomous Vehicles (India)

Console-first, safety-aware ADAS research scaffold for real-time Indian road sign detection, classification, and LLM-driven interpretation. Built for edge/Jetson targets with OpenCV + YOLOv8/YOLOv9 (with EfficientDet/SSD fallbacks), high-accuracy classifiers (ResNet50, EfficientNet-B4, MobileNetV3, ViT), and Rich-powered TUI for live feedback.

## Features
- Multi-stage pipeline: OpenCV preprocessing → detector (YOLOv8/YOLOv9, EfficientDet, SSD MobileNet) → classifier (ResNet50/EfficientNet-B4/MobileNetV3/ViT) → LLM explanation and driving hints.
- Safety-first console UI: color-coded alerts, confidence thresholds, FPS/latency/accuracy display, manual overrides and graceful degradation.
- Optimization hooks: transfer learning on Indian datasets (ITSD, IDTSR, Mapillary India, AI4Bharat, dashcam), hyperparameter tuning, quantization (INT8/FP16), pruning, knowledge distillation, ONNX Runtime, CPU/GPU hybrid, Jetson-friendly paths.
- Deployment-ready: Docker, ONNX export hooks, modular backends for detectors/classifiers/LLM.

## Quickstart (dev loop)
1) Install Python 3.10+ and a GPU build of PyTorch (or CPU if needed).
2) Create a venv, then install deps:
```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```
3) Run the console dashboard (webcam 0 by default):
```bash
python -m src.main --source 0
```
4) To use a prerecorded video: `python -m src.main --source path/to/video.mp4`.
5) Provide an OpenAI/HuggingFace key via env var `LLM_API_KEY` to enable explanations. Without it, the LLM layer will emit stub text.

## Project layout
- `src/config.py` – runtime configuration dataclasses.
- `src/pipeline.py` – orchestrates detection → classification → LLM reasoning.
- `src/ui/dashboard.py` – Rich-based TUI with adaptive layout and alerts.
- `src/utils/*` – video capture, metrics, safety logic, types.
- `src/detectors/*` – detector backends (YOLO, EfficientDet, SSD MobileNet).
- `src/classifiers/*` – classifier backends (ResNet, EfficientNet, MobileNetV3, ViT).
- `src/llm/explainer.py` – LLM wrapper for sign explanations and driving hints.
- `src/optimization/optim_utils.py` – optimization stubs (quantization/pruning/distillation).
- `Dockerfile` – edge-ready container base for CPU/GPU.

## Notes on datasets and training
- Prepare data with ITSD, IDTSR, Mapillary India, AI4Bharat, or custom dashcam captures.
- Fine-tune detectors/classifiers with transfer learning hooks in `optimization/optim_utils.py`.
- Export ONNX/INT8/FP16 for Jetson/edge using provided stubs; plug in your calibration dataloaders.

## Safety considerations
- Confidence thresholds and degradation modes block low-confidence actions.
- Manual override flag to bypass automation in research setups.
- The TUI surfaces alerts when FPS drops, GPU is missing, or detections are uncertain.

## Roadmap suggestions
- Wire actual training scripts for each model family.
- Add dataset loaders and evaluation harnesses.
- Integrate TensorRT / OpenVINO builds for lower latency.
- Extend to multi-camera fusion and map alignment.
