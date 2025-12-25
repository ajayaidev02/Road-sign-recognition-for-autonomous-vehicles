# Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Train the Model (Optional)
If you want to train a new model from your dataset:

```bash
python training/train.py
```

**What this does:**
- Loads all images from `dataset/train/images/` and `dataset/train/labels/`
- Creates and trains a CNN model
- Saves the model to `models/traffic_sign_model.h5`
- Generates accuracy and loss graphs in `outputs/`
- Takes approximately 5-10 minutes on a typical machine

**Expected Output:**
- Training Accuracy: 50-60%
- Validation Accuracy: 75-80%
- Loss graphs showing convergence

### Step 3: Run the Application
```bash
python main.py
```

## Using the GUI Application

1. **Click "Browse Image"** - Select a traffic sign image from your computer
2. **Click "Classify"** - The model will predict the traffic sign type
3. **View Result** - The recognized sign name will appear in the text box

## Folder Structure

After running `training/train.py`, you'll have:

```
project/
├── models/
│   └── traffic_sign_model.h5       ← Generated trained model
├── outputs/
│   ├── accuracy.png                ← Training accuracy graph
│   └── loss.png                    ← Training loss graph
├── dataset/
│   ├── train/                      ← Your training data
│   └── test/                       ← Your test data
└── [other files]
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Run `pip install -r requirements.txt` |
| No dataset found | Place your dataset in `dataset/train/` with `images/` and `labels/` folders |
| Model not found | Run `python training/train.py` to train and generate the model |
| GUI not opening | Try running with `python -m PyQt5.uic` to check PyQt5 installation |

## Files Explained

- `main.py` - GUI application for image classification
- `training/train.py` - Standalone training script
- `utils/` - Helper modules (data loading, model architecture, class definitions)
- `dataset/` - Your YOLO format dataset
- `models/` - Saved trained models
- `outputs/` - Training results and graphs

## Next Steps

1. **Improve Accuracy:** Train for more epochs, adjust hyperparameters in `training/train.py`
2. **Data Augmentation:** Add image augmentation in `utils/data_loader.py`
3. **Real-time Detection:** Extend the project to detect signs in video streams
4. **Deployment:** Convert the model to TensorFlow Lite for mobile devices

---

For detailed information, see [SETUP.md](SETUP.md)
