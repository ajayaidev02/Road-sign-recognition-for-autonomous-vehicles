# Project Organization Overview

## What's New

Your project has been reorganized into a modular, professional structure:

### 📁 **New Folder Structure**

```
Road sign recognition for autonomous vehicles/
│
├── 📄 main.py                      # GUI Application (unchanged core functionality)
├── 📄 QUICKSTART.md               # ⭐ Read this first!
├── 📄 SETUP.md                    # Detailed setup and usage guide
│
├── 📁 training/                   # ⭐ NEW: Dedicated training module
│   ├── train.py                   # Standalone training script
│   └── __init__.py
│
├── 📁 utils/                      # ⭐ NEW: Shared utilities
│   ├── __init__.py
│   ├── data_loader.py             # Dataset loading functions
│   ├── model.py                   # Model architecture
│   └── classes.py                 # Traffic sign definitions
│
├── 📁 models/                     # ⭐ NEW: Models storage
│   └── (trained models saved here)
│
├── 📁 outputs/                    # ⭐ NEW: Training outputs
│   ├── accuracy.png               # Training accuracy graph
│   └── loss.png                   # Training loss graph
│
├── 📁 dataset/                    # Your dataset (unchanged)
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   └── test/
│       ├── images/
│       └── labels/
│
└── (other original files)
```

---

## 🎯 How to Use

### For Training
```bash
cd "Road sign recognition for autonomous vehicles"
python training/train.py
```

- **Location:** `training/train.py`
- **Input:** Reads from `dataset/train/images/` and `dataset/train/labels/`
- **Output:** 
  - Trained model → `models/traffic_sign_model.h5`
  - Graphs → `outputs/accuracy.png` and `outputs/loss.png`

### For GUI/Classification
```bash
python main.py
```

- **Location:** `main.py` (main directory)
- **Features:** Browse, load, and classify images
- **Uses:** Pre-trained model from `models/` folder

---

## 📚 Module Breakdown

### `utils/data_loader.py`
Handles dataset loading and preprocessing:
- `load_dataset()` - Loads YOLO format dataset
- `prepare_training_data()` - Splits and one-hot encodes labels

### `utils/model.py`
Contains model architecture:
- `create_model()` - Creates CNN architecture
- `compile_model()` - Compiles with optimizer and loss function

### `utils/classes.py`
Traffic sign class mappings:
- `TRAFFIC_SIGNS` - Dictionary of 43 sign classes
- `get_sign_name()` - Function to get sign name from ID
- `NUM_CLASSES` - Total number of classes (43)

### `training/train.py`
Complete training pipeline:
- Loads data automatically from `dataset/train/`
- Creates model from scratch
- Trains for up to 15 epochs with early stopping
- Saves model and generates performance graphs
- Prints detailed metrics

---

## ✨ Benefits of This Organization

| Before | After |
|--------|-------|
| Everything in one file | Modular, organized structure |
| Hard to maintain | Easy to update utilities |
| Class definitions scattered | Centralized in `utils/classes.py` |
| Training in GUI | Separated to `training/train.py` |
| Model hardcoded | Reusable model creation function |
| Dataset loading mixed with GUI | Dedicated `data_loader.py` |

---

## 🔄 Workflow

### Development Workflow
```
1. Update dataset in dataset/train/ and dataset/test/
2. Run: python training/train.py
3. Check: outputs/accuracy.png and outputs/loss.png
4. Use best model in GUI: python main.py
```

### Extension Points
- Want to add data augmentation? → Edit `utils/data_loader.py`
- Want to change model architecture? → Edit `utils/model.py`
- Want to add new classes? → Update `utils/classes.py`
- Want to modify training? → Edit `training/train.py`

---

## 🚀 Next Steps

1. **Read QUICKSTART.md** - Get running in 3 steps
2. **Explore the code** - Each utility file is well-documented
3. **Train a model** - `python training/train.py`
4. **Use the GUI** - `python main.py`
5. **Customize** - Modify utilities for your needs

---

## 📝 File Descriptions

| File | Purpose | Edit When |
|------|---------|-----------|
| `main.py` | GUI interface | Want to change UI |
| `training/train.py` | Model training | Want to adjust training parameters |
| `utils/data_loader.py` | Dataset loading | Want to add augmentation |
| `utils/model.py` | Model architecture | Want to change model layers |
| `utils/classes.py` | Class definitions | Want to add/modify traffic signs |

---

## 💡 Tips

✅ **Keep `dataset/` and `models/` clean:**
- All training happens in separate modules
- Models are saved automatically to `models/`
- Keep original dataset intact

✅ **Reuse utilities:**
- Import from utils in your own scripts
- Example: `from utils import load_dataset, create_model`

✅ **Monitor training:**
- Check `outputs/` folder after training
- Graphs show if model is learning correctly

---

**Version:** 2.0  
**Last Updated:** December 25, 2025  
**Status:** ✅ Production Ready
