"""
Data loading utilities for the road sign recognition project.
Handles loading YOLO format datasets and preprocessing images.
"""

import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical


def load_dataset(dataset_path, num_classes=43, img_size=30):
    """
    Load images and labels from YOLO format dataset.
    
    Args:
        dataset_path: Path to dataset folder containing 'images' and 'labels' subdirectories
        num_classes: Number of classes (default: 43 for traffic signs)
        img_size: Target image size in pixels (default: 30)
    
    Returns:
        data: Numpy array of images
        labels: Numpy array of class labels
    """
    data = []
    labels = []
    
    images_path = os.path.join(dataset_path, 'images')
    labels_path = os.path.join(dataset_path, 'labels')
    
    if not os.path.exists(images_path) or not os.path.exists(labels_path):
        print(f"Error: Dataset paths not found at {dataset_path}")
        return np.array([]), np.array([])
    
    # Get all image files
    image_files = [f for f in os.listdir(images_path) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Found {len(image_files)} images to load...")
    
    for idx, image_file in enumerate(image_files):
        try:
            # Get corresponding label file
            label_file = os.path.splitext(image_file)[0] + '.txt'
            label_path = os.path.join(labels_path, label_file)
            
            if os.path.exists(label_path):
                # Read the label file (YOLO format: class_id x_center y_center width height)
                with open(label_path, 'r') as f:
                    line = f.readline().strip()
                    if line:
                        class_id = int(line.split()[0])
                        
                        # Load and process image
                        image = Image.open(os.path.join(images_path, image_file))
                        image = image.resize((img_size, img_size))
                        image = np.array(image)
                        data.append(image)
                        labels.append(class_id)
                        
                        if (idx + 1) % 500 == 0:
                            print(f"  Loaded {idx + 1} images...")
            else:
                print(f"Warning: Label file not found for {image_file}")
        except Exception as e:
            print(f"Error loading image {image_file}: {str(e)}")
    
    print(f"Total images loaded: {len(data)}")
    return np.array(data), np.array(labels)


def prepare_training_data(data, labels, test_size=0.2, num_classes=43):
    """
    Prepare training and testing datasets with one-hot encoding.
    
    Args:
        data: Numpy array of images
        labels: Numpy array of class labels
        test_size: Fraction of data to use for testing (default: 0.2)
        num_classes: Number of classes (default: 43)
    
    Returns:
        X_train, X_test, y_train, y_test: Prepared datasets with one-hot encoded labels
    """
    if len(data) == 0:
        print("Error: No data to prepare")
        return None, None, None, None
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        data, labels, test_size=test_size, random_state=42
    )
    
    # Convert labels to one-hot encoding
    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)
    
    print(f"Training set: {X_train.shape}, Testing set: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test
