# Quick Start Guide (No Virtual Environment)

## Setup Complete! ✓

The virtual environment has been removed and the project is now configured to run using your system Python installation.

## Current Configuration
- **Python Version**: 3.9.6
- **Python Path**: C:\Users\ajayo\AppData\Local\Programs\Python\Python39\python.exe
- **Dependencies**: All installed to system Python

## Running the Project

### 1. Basic Usage (Webcam)
```powershell
python -m src.main --source 0
```

### 2. Using a Video File
```powershell
python -m src.main --source "path\to\video.mp4"
```

### 3. With Custom Detector and Classifier
```powershell
python -m src.main --source 0 --detector yolov8n --classifier resnet50
```

### 4. Available Options
- `--source`: Camera index (0, 1, etc.) or video file path
- `--detector`: yolov8n, yolov9c, efficientdet_d0, ssd_mobilenet_v3
- `--classifier`: resnet50, efficientnet_b4, mobilenet_v3_large, vit_b_16
- `--max-frames`: Stop after N frames
- `--no-preview`: Disable preview (TUI only)
- `--target-fps`: Target capture FPS
- `--queue`: Frame queue size

### 5. Enable LLM Explanations (Optional)
Set the environment variable for OpenAI/HuggingFace API:
```powershell
$env:LLM_API_KEY="your-api-key-here"
python -m src.main --source 0
```

## Testing the Setup
```powershell
# Show help
python -m src.main --help

# Check installed packages
pip list | Select-String "torch|opencv|ultralytics"
```

## File Structure Created
The following utility modules were added to complete the project:
- `src/utils/preprocess.py` - Image preprocessing utilities
- `src/utils/tracker.py` - Object tracking across frames
- `src/utils/controls.py` - Control state and keyboard input handling

## Notes
- All dependencies are now installed in your system Python (not in a virtual environment)
- Make sure you're in the project directory when running commands
- If you need to reinstall dependencies: `pip install -r requirements.txt`
