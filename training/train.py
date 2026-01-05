"""
Training script for the road sign recognition model.
Run this script separately to train the model and save it to the models/ folder.
"""

import os
import sys
import argparse
import datetime
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, TensorBoard
from keras.preprocessing.image import ImageDataGenerator

# Add parent directory to path to import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_dataset, prepare_training_data
from utils.model import create_model, compile_model
from utils.classes import NUM_CLASSES
from utils.config import BATCH_SIZE, EPOCHS, AUGMENTATION, AUGMENTATION_PARAMS, IMG_SIZE, INPUT_SHAPE, USE_TRANSFER_LEARNING, LEARNING_RATE, FINE_TUNE_AT


def main(args):
    """Main training function."""
    
    # Get paths
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = args.dataset if args.dataset else os.path.join(current_dir, 'dataset', 'train')
    models_dir = args.models_dir if args.models_dir else os.path.join(current_dir, 'models')
    
    print("=" * 60)
    print("Road Sign Recognition - Training Script")
    print("=" * 60)
    
    # Create models directory if it doesn't exist
    os.makedirs(models_dir, exist_ok=True)
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print(f"\nError: Dataset not found at {dataset_path}")
        print("Please ensure you have the dataset folder with 'images' and 'labels' subdirectories.")
        return
    
    print(f"\nDataset path: {dataset_path}")
    print(f"Models directory: {models_dir}")
    
    # Load dataset
    print("\n" + "-" * 60)
    print("Loading dataset...")
    print("-" * 60)
    data, labels = load_dataset(dataset_path, num_classes=NUM_CLASSES, img_size=IMG_SIZE)
    
    if len(data) == 0:
        print("Error: No data loaded. Exiting.")
        return
    
    # Prepare training data
    print("\n" + "-" * 60)
    print("Preparing training data...")
    print("-" * 60)
    X_train, X_test, y_train, y_test = prepare_training_data(
        data, labels, test_size=0.2, num_classes=NUM_CLASSES
    )
    
    if X_train is None:
        print("Error: Failed to prepare data. Exiting.")
        return
    
    # Create and compile model
    print("\n" + "-" * 60)
    print("Creating and compiling model...")
    print("-" * 60)
    model_type = args.model_type if hasattr(args, 'model_type') and args.model_type else 'auto'
    model = create_model(num_classes=NUM_CLASSES, input_shape=INPUT_SHAPE, model_type=model_type)
    # create_model may already return a compiled transfer model; only compile if uncompiled
    # model.optimizer exists on Keras models but may be None if not compiled
    if not hasattr(model, 'optimizer') or model.optimizer is None:
        model = compile_model(model)
    print("Model created successfully!")
    print(f"Total parameters: {model.count_params():,}")
    
    # Setup callbacks
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2,
        min_lr=1e-7,
        verbose=1
    )

    # ModelCheckpoint and TensorBoard
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    checkpoint_path = os.path.join(models_dir, f'traffic_sign_best_{timestamp}.h5')
    checkpoint_cb = ModelCheckpoint(
        checkpoint_path,
        monitor='val_loss',
        save_best_only=True,
        save_weights_only=False,
        verbose=1
    )

    logs_dir = os.path.join(current_dir, 'outputs', 'logs', timestamp)
    os.makedirs(logs_dir, exist_ok=True)
    tensorboard_cb = TensorBoard(log_dir=logs_dir)
    
    # Train model
    print("\n" + "-" * 60)
    print("Training model...")
    print("-" * 60)
    if args.batch_size:
        batch_size = args.batch_size
    else:
        batch_size = BATCH_SIZE

    if args.epochs:
        epochs = args.epochs
    else:
        epochs = EPOCHS

    if AUGMENTATION:
        print("Using data augmentation for training.")
        datagen = ImageDataGenerator(**AUGMENTATION_PARAMS)
        datagen.fit(X_train)
        steps_per_epoch = max(1, len(X_train) // batch_size)
        history = model.fit(
            datagen.flow(X_train, y_train, batch_size=batch_size),
            steps_per_epoch=steps_per_epoch,
            epochs=epochs,
            validation_data=(X_test, y_test),
            callbacks=[early_stopping, reduce_lr, checkpoint_cb, tensorboard_cb],
            verbose=1
        )
    else:
        history = model.fit(
            X_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(X_test, y_test),
            callbacks=[early_stopping, reduce_lr, checkpoint_cb, tensorboard_cb],
            verbose=1
        )
    
    # Save model
    print("\n" + "-" * 60)
    print("Saving model...")
    print("-" * 60)
    # Save HDF5
    model_path = os.path.join(models_dir, f'traffic_sign_model_{timestamp}.h5')
    model.save(model_path)
    print(f"Model saved to: {model_path}")

    # Optionally export SavedModel format
    if args.export_savedmodel:
        saved_model_dir = os.path.join(models_dir, f'traffic_sign_savedmodel_{timestamp}')
        model.save(saved_model_dir, save_format='tf')
        print(f"SavedModel exported to: {saved_model_dir}")

    # Optionally export TFLite
    if args.export_tflite:
        try:
            converter = tf.lite.TFLiteConverter.from_keras_model(model)
            tflite_model = converter.convert()
            tflite_path = os.path.join(models_dir, f'traffic_sign_{timestamp}.tflite')
            with open(tflite_path, 'wb') as f:
                f.write(tflite_model)
            print(f"TFLite model saved to: {tflite_path}")
        except Exception as e:
            print(f"Warning: TFLite conversion failed: {e}")
    
    # Create outputs directory for graphs
    outputs_dir = os.path.join(current_dir, 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Plot and save accuracy graph
    print("\nGenerating accuracy graph...")
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    plt.title('Model Accuracy', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    accuracy_path = os.path.join(outputs_dir, 'accuracy.png')
    plt.savefig(accuracy_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Accuracy graph saved to: {accuracy_path}")
    
    # Plot and save loss graph
    print("Generating loss graph...")
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Training Loss', linewidth=2)
    plt.plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
    plt.title('Model Loss', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    loss_path = os.path.join(outputs_dir, 'loss.png')
    plt.savefig(loss_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Loss graph saved to: {loss_path}")
    
    # Print final metrics
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"Final Training Accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")
    print(f"Final Training Loss: {history.history['loss'][-1]:.4f}")
    print(f"Final Validation Loss: {history.history['val_loss'][-1]:.4f}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train traffic sign recognition model')
    parser.add_argument('--dataset', type=str, help='Path to dataset folder (images + labels)')
    parser.add_argument('--models-dir', type=str, help='Directory to save trained models')
    parser.add_argument('--batch-size', type=int, help='Batch size to use for training')
    parser.add_argument('--epochs', type=int, help='Number of training epochs')
    parser.add_argument('--export-savedmodel', action='store_true', help='Also export SavedModel format')
    parser.add_argument('--export-tflite', action='store_true', help='Also export TFLite model')
    parser.add_argument('--model-type', type=str, choices=['auto', 'small', 'high', 'transfer'],
                        help="Model architecture to use: 'auto' (default/transfer if enabled), 'small', 'high', or 'transfer'")
    args = parser.parse_args()
    main(args)
