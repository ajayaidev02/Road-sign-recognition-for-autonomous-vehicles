"""
Configuration constants for the project.
"""
VERSION = "2.0"

# Image and training parameters
IMG_SIZE = 30
BATCH_SIZE = 32
EPOCHS = 25

# Enable simple training-time augmentation
AUGMENTATION = True
AUGMENTATION_PARAMS = {
    'rotation_range': 15,
    'width_shift_range': 0.1,
    'height_shift_range': 0.1,
    'zoom_range': 0.1,
    'horizontal_flip': False,
    'brightness_range': (0.8, 1.2)
}

# Optimizer / scheduler choices can be expanded later
LEARNING_RATE = 1e-3
