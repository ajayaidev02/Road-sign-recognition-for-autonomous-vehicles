# 🎯 Project Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│     Road Sign Recognition for Autonomous Vehicles          │
└─────────────────────────────────────────────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                        │
         ┌───────▼────────┐       ┌───────▼────────┐
         │   main.py      │       │  training/     │
         │  (GUI App)     │       │  train.py      │
         │                │       │  (Training)    │
         └───────┬────────┘       └────────┬────────┘
                 │                        │
                 └────────────┬───────────┘
                              │
                    ┌─────────▼─────────┐
                    │   utils/          │
                    │  (Shared Code)    │
                    │  - data_loader.py │
                    │  - model.py       │
                    │  - classes.py     │
                    └───────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
      ┌────▼────┐       ┌─────▼─────┐      ┌────▼────┐
      │ dataset/ │       │ models/   │      │ outputs/│
      │(Data)   │       │(Models)   │      │(Results)│
      └──────────┘       └───────────┘      └─────────┘
```

---

## Data Flow: Training Pipeline

```
dataset/train/
  ├── images/          ────────┐
  └── labels/                  │
                              │
                        ┌─────▼──────────┐
                        │ data_loader.py │
                        │ (Load dataset) │
                        └─────┬──────────┘
                              │
                        ┌─────▼──────────┐
                        │  Prepare data  │
                        │ (80/20 split)  │
                        └─────┬──────────┘
                              │
                        ┌─────▼──────────┐
                        │   model.py     │
                        │ (Create model) │
                        └─────┬──────────┘
                              │
                        ┌─────▼──────────┐
                        │  Training loop │
                        │  (15 epochs)   │
                        └─────┬──────────┘
                              │
                    ┌─────────┴──────────┐
                    │                    │
              ┌─────▼─────┐      ┌───────▼────────┐
              │ models/   │      │   outputs/     │
              │  model.h5 │      │  accuracy.png  │
              └───────────┘      │  loss.png      │
                                 └────────────────┘
```

---

## Data Flow: GUI Classification Pipeline

```
Image File (User selects)
          │
    ┌─────▼──────────┐
    │  main.py       │
    │  (Browse Image)│
    └─────┬──────────┘
          │
    ┌─────▼──────────────┐
    │ Load Pre-trained   │
    │ Model (.h5 file)   │
    └─────┬──────────────┘
          │
    ┌─────▼──────────────┐
    │ Preprocess Image   │
    │ (30x30 resize)     │
    └─────┬──────────────┘
          │
    ┌─────▼──────────────┐
    │ Model Prediction   │
    │ (Forward pass)     │
    └─────┬──────────────┘
          │
    ┌─────▼──────────────┐
    │ classes.py         │
    │ (Decode prediction)│
    └─────┬──────────────┘
          │
    ┌─────▼──────────────┐
    │ Display Result     │
    │ (Sign name in GUI) │
    └────────────────────┘
```

---

## Module Dependencies

```
main.py (GUI Application)
    ├── utils.classes
    │   └── TRAFFIC_SIGNS (sign definitions)
    ├── keras.models.load_model
    │   └── uses: models/traffic_sign_model.h5
    └── PIL (image loading)

training/train.py (Training Script)
    ├── utils.data_loader
    │   ├── load_dataset()
    │   └── prepare_training_data()
    ├── utils.model
    │   ├── create_model()
    │   └── compile_model()
    ├── utils.classes
    │   └── NUM_CLASSES
    ├── keras (training)
    └── matplotlib (graphs)

utils/
    ├── __init__.py (exports all functions)
    ├── data_loader.py (dataset operations)
    ├── model.py (model architecture)
    └── classes.py (class definitions)
```

---

## Folder Tree

```
Road sign recognition for autonomous vehicles/
│
├── 🎯 main.py                    ← GUI application
├── 📚 QUICKSTART.md              ← Start here
├── 📖 SETUP.md                   ← Full documentation
├── 📊 PROJECT_ORGANIZATION.md    ← Structure explanation
├── ✨ TRAINING_SETUP_COMPLETE.md ← This setup summary
│
├── 📁 training/                  ← Training module
│   ├── train.py                  ← Training script
│   └── __init__.py
│
├── 📁 utils/                     ← Shared utilities
│   ├── __init__.py               ← Package init
│   ├── data_loader.py            ← Dataset loading
│   ├── model.py                  ← Model architecture
│   └── classes.py                ← Sign definitions
│
├── 📁 dataset/                   ← Your data
│   ├── train/
│   │   ├── images/               ← Training images
│   │   └── labels/               ← Training labels
│   └── test/
│       ├── images/               ← Test images
│       └── labels/               ← Test labels
│
├── 📁 models/                    ← Saved models
│   └── traffic_sign_model.h5     ← Latest trained model
│
├── 📁 outputs/                   ← Training results
│   ├── accuracy.png              ← Accuracy curve
│   └── loss.png                  ← Loss curve
│
├── 📁 __pycache__/               ← Python cache
│
├── my_model.h5                   ← Pre-trained model
├── my_model_new.h5               ← Alternative model
├── Accuracy1.png                 ← Previous results
├── Loss1.png                     ← Previous results
└── requirements.txt              ← Dependencies
```

---

## Class Diagram: Model Architecture

```
┌─────────────────────────────────┐
│     CNN Model (242K params)     │
├─────────────────────────────────┤
│ Input Layer                     │
│  └─ Shape: (30, 30, 3)         │
├─────────────────────────────────┤
│ Conv Block 1                    │
│  ├─ Conv2D: 32 filters, 5x5    │
│  ├─ Conv2D: 32 filters, 5x5    │
│  ├─ MaxPool2D: 2x2             │
│  └─ Dropout: 0.25              │
├─────────────────────────────────┤
│ Conv Block 2                    │
│  ├─ Conv2D: 64 filters, 3x3    │
│  ├─ Conv2D: 64 filters, 3x3    │
│  ├─ MaxPool2D: 2x2             │
│  └─ Dropout: 0.25              │
├─────────────────────────────────┤
│ Dense Layers                    │
│  ├─ Flatten                     │
│  ├─ Dense: 256, ReLU           │
│  ├─ Dropout: 0.5               │
│  └─ Dense: 43, Softmax         │
├─────────────────────────────────┤
│ Output Layer                    │
│  └─ Shape: (43,) - Sign class  │
└─────────────────────────────────┘
```

---

## Training Process Flow

```
Start
  │
  ├─► Load dataset (2200+ images)
  │     └─ 80% training, 20% validation
  │
  ├─► Create CNN model
  │     └─ 242,251 parameters
  │
  ├─► Compile model
  │     └─ Adam optimizer, categorical crossentropy loss
  │
  ├─► Train (up to 15 epochs)
  │     ├─ Epoch 1-5: Rapid improvement
  │     ├─ Epoch 6-10: Gradual refinement
  │     ├─ Epoch 11-15: Fine-tuning (if no improvement → early stop)
  │     └─ Learning rate adjustment on plateau
  │
  ├─► Evaluate on validation set
  │     └─ Display accuracy and loss
  │
  ├─► Save model
  │     └─ models/traffic_sign_model.h5
  │
  └─► Generate graphs
        ├─ outputs/accuracy.png
        └─ outputs/loss.png
```

---

## Key Features Map

```
┌──────────────────────────────────────────────────┐
│         PROJECT CAPABILITIES                    │
├──────────────────────────────────────────────────┤
│                                                 │
│  Training              GUI              Utils   │
│  ────────              ───              ─────   │
│  • Dataset load        • Image select   • Data  │
│  • Model create        • Classify       • Model │
│  • Optimization        • Train          • Class │
│  • Evaluation          • Results        │       │
│  • Graph gen           • Display        │       │
│                                         │       │
└──────────────────────────────────────────────────┘
```

---

## Deployment Ready

```
Production Usage
       │
       ├─► GUI Application (main.py)
       │   └─ For interactive classification
       │
       └─► Training Pipeline (training/train.py)
           └─ For continuous improvement
               └─ Real-time monitoring
               └─ Model versioning
               └─ Performance tracking
```

---

**Note:** This diagram shows the complete architecture of the reorganized project.
All components are modular and can be extended independently.

For more details, see:
- QUICKSTART.md - Quick setup guide
- SETUP.md - Complete documentation
- PROJECT_ORGANIZATION.md - Folder structure details
