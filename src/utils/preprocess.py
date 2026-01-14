"""Image preprocessing utilities for road sign detection."""

import cv2
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import PreprocessConfig


def preprocess_frame(frame: np.ndarray, cfg: 'PreprocessConfig' = None, target_size: tuple = (640, 640)) -> np.ndarray:
    """
    Preprocess a frame for detection and classification.
    
    Args:
        frame: Input image frame (BGR format from OpenCV)
        cfg: Preprocessing configuration object
        target_size: Target size for resizing (width, height)
    
    Returns:
        Preprocessed frame
    """
    if frame is None:
        raise ValueError("Input frame is None")
    
    # Resize frame to target size
    processed = cv2.resize(frame, target_size, interpolation=cv2.INTER_LINEAR)
    
    # If no config provided, use default processing
    if cfg is None:
        # Apply basic CLAHE
        lab = cv2.cvtColor(processed, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        processed = cv2.merge([l, a, b])
        processed = cv2.cvtColor(processed, cv2.COLOR_LAB2BGR)
        return processed
    
    # Apply CLAHE for contrast enhancement
    if cfg.enable_clahe:
        lab = cv2.cvtColor(processed, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        processed = cv2.merge([l, a, b])
        processed = cv2.cvtColor(processed, cv2.COLOR_LAB2BGR)
    
    # Apply Gaussian blur for noise reduction
    if cfg.enable_blur:
        processed = cv2.GaussianBlur(processed, (cfg.blur_kernel, cfg.blur_kernel), 0)
    
    # Apply bilateral filter
    if cfg.enable_bilateral:
        processed = cv2.bilateralFilter(processed, 9, 75, 75)
    
    # Apply sharpening
    if cfg.enable_sharpen:
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        processed = cv2.filter2D(processed, -1, kernel)
    
    # Apply gamma correction
    if cfg.enable_gamma:
        inv_gamma = 1.0 / cfg.gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
        processed = cv2.LUT(processed, table)
    
    return processed
