import cv2
import numpy as np


def enhance_document(image):

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # --------------------------------------------------
    # STEP 1: Contrast Stretching
    # (MATLAB: imadjust)
    # --------------------------------------------------

    contrast = cv2.normalize(
        gray,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    # --------------------------------------------------
    # STEP 2: Unsharp Masking
    # (MATLAB: imsharpen)
    # --------------------------------------------------

    blurred = cv2.GaussianBlur(
        contrast,
        (0, 0),
        3
    )

    sharpened = cv2.addWeighted(
        contrast,
        1.8,
        blurred,
        -0.8,
        0
    )

    # --------------------------------------------------
    # STEP 3: Adaptive Binarization
    # (MATLAB: imbinarize adaptive)
    # --------------------------------------------------

    binary = cv2.adaptiveThreshold(
        sharpened,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

    # --------------------------------------------------
    # STEP 4: Small Noise Removal
    # --------------------------------------------------

    kernel = np.ones(
        (2, 2),
        np.uint8
    )

    cleaned = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        kernel
    )

    return cleaned