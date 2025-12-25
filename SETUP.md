# Road Sign Recognition for Autonomous Vehicles

A deep learning project for recognizing and classifying 43 different traffic signs using a CNN model trained on the GTSRB (German Traffic Sign Recognition Benchmark) dataset.

## Project Structure

```
Road sign recognition for autonomous vehicles/
├── main.py                          # GUI Application
├── my_model.h5                      # Pre-trained model
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
│
├── dataset/                         # Dataset folder (YOLO format)
│   ├── train/
│   │   ├── images/                  # Training images
│   │   └── labels/                  # Training labels (YOLO format)
│   └── test/
│       ├── images/                  # Test images
│       └── labels/                  # Test labels (YOLO format)
│
├── training/                        # Training module
│   ├── train.py                     # Standalone training script
│   └── __init__.py
│
├── models/                          # Saved models directory
│   └── traffic_sign_model.h5        # Model output from training
│
├── outputs/                         # Training outputs
│   ├── accuracy.png                 # Accuracy graph
│   └── loss.png                     # Loss graph
│
└── utils/                           # Utility modules
    ├── __init__.py
    ├── data_loader.py               # Dataset loading functions
    ├── model.py                     # Model architecture
    └── classes.py                   # Traffic sign class definitions
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Dataset Structure

Ensure your dataset is organized in YOLO format:
- `dataset/train/images/` - Contains training images
- `dataset/train/labels/` - Contains YOLO format label files (.txt)
- `dataset/test/images/` - Contains test images
- `dataset/test/labels/` - Contains YOLO format label files (.txt)

Each label file should contain: `class_id x_center y_center width height` (normalized coordinates)

## Usage

### Run the GUI Application

```bash
python main.py
```

This launches the PyQt5 GUI with three main features:
- **Browse Image**: Select an image from your computer
- **Classify**: Predict the traffic sign class using the pre-trained model
- **Training**: Train a new model from scratch (requires dataset)

### Train a New Model

To train a new model from the dataset:

```bash
python training/train.py
```

**Features:**
- Loads YOLO format dataset automatically
- Creates a CNN model from scratch
- Trains for up to 15 epochs with early stopping
- Saves the model to `models/traffic_sign_model.h5`
- Generates training graphs (accuracy and loss)
- Provides detailed training metrics

**Expected Results:**
- Training accuracy: ~54-60% on first 5 epochs
- Validation accuracy: ~75% on first 5 epochs
- Further training improves accuracy

**Output Files:**
- `models/traffic_sign_model.h5` - Trained model
- `outputs/accuracy.png` - Accuracy graph
- `outputs/loss.png` - Loss graph

## Model Architecture

The CNN model consists of:
1. **First Convolutional Block**
   - Conv2D: 32 filters, 5x5 kernel
   - Conv2D: 32 filters, 5x5 kernel
   - MaxPool2D: 2x2
   - Dropout: 0.25

2. **Second Convolutional Block**
   - Conv2D: 64 filters, 3x3 kernel
   - Conv2D: 64 filters, 3x3 kernel
   - MaxPool2D: 2x2
   - Dropout: 0.25

3. **Fully Connected Layers**
   - Dense: 256 units, ReLU activation
   - Dropout: 0.5
   - Dense: 43 units, Softmax activation (output layer)

**Input:** 30x30 RGB images
**Output:** 43 traffic sign classes

## Traffic Sign Classes

The model recognizes 43 different traffic signs including:
- Speed limits (20-120 km/h)
- Yield, Stop, Priority road
- No entry, No passing
- Turn right/left, Go straight
- Pedestrians, Bicycles, Children crossing
- Dangerous curves, Bumpy road, Slippery road
- And more...

See `utils/classes.py` for the complete list.

## Dependencies

- Python 3.7+
- TensorFlow/Keras
- NumPy
- Pillow (PIL)
- scikit-learn
- PyQt5
- Matplotlib

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Training Data

The project uses the GTSRB (German Traffic Sign Recognition Benchmark) dataset in YOLO format:
- **Training images:** 5000+ images across 43 classes
- **Test images:** 1000+ images across 43 classes
- **Image size:** 30x30 pixels
- **Format:** RGB

## Tips for Better Results

1. **Data Augmentation:** Consider adding data augmentation (rotation, brightness, noise) to improve robustness
2. **Longer Training:** Train for more epochs (15+) to achieve higher accuracy
3. **Hyperparameter Tuning:** Adjust learning rate, batch size, and dropout rates
4. **Image Preprocessing:** Normalize pixel values to [0, 1] range for better convergence

## Troubleshooting

**Problem:** "Dataset folder not found"
- **Solution:** Ensure dataset is in `dataset/` folder with proper structure

**Problem:** Model file not found
- **Solution:** Run `training/train.py` to train and generate the model, or ensure `my_model.h5` exists

**Problem:** Out of memory errors
- **Solution:** Reduce batch size in `training/train.py` (line with `batch_size=32`)

## File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | PyQt5 GUI application for classification |
| `training/train.py` | Standalone script to train new models |
| `utils/data_loader.py` | Functions for loading YOLO format datasets |
| `utils/model.py` | CNN model architecture |
| `utils/classes.py` | Traffic sign class definitions |

## License

This project is for educational purposes.

## References

- GTSRB Dataset: http://benchmark.ini.rub.de/?section=gtsrb
- TensorFlow/Keras: https://www.tensorflow.org/
- PyQt5: https://www.riverbankcomputing.com/software/pyqt/

---

**Last Updated:** December 2025
