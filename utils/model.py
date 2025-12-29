"""
Model architecture utilities for the road sign recognition project.
Defines the CNN model structure and provides functions for model management.
"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout
from .config import IMG_SIZE


def create_model(num_classes=43, input_shape=(30, 30, 3)):
    """
    Create a CNN model for traffic sign classification.
    
    Args:
        num_classes: Number of output classes (default: 43 for traffic signs)
    
    Returns:
        model: Compiled Keras Sequential model
    """
    model = Sequential()
    
    # First convolutional block
    model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu', 
                     input_shape=input_shape))
    model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(rate=0.25))
    
    # Second convolutional block
    model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(rate=0.25))
    
    # Fully connected layers
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(rate=0.5))
    model.add(Dense(num_classes, activation='softmax'))
    
    return model


def compile_model(model, loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']):
    """
    Compile the model with specified loss and optimizer.
    
    Args:
        model: Keras model to compile
        loss: Loss function (default: 'categorical_crossentropy')
        optimizer: Optimizer (default: 'adam')
        metrics: Metrics to track (default: ['accuracy'])
    
    Returns:
        model: Compiled model
    """
    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    return model
