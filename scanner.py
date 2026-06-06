import cv2
import numpy as np

from document_detector import detect_document


def order_points(pts):
    """
    Order 4 points as:
    [top-left, top-right, bottom-right, bottom-left]
    """

    rect = np.zeros(
        (4, 2),
        dtype="float32"
    )

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]   # smallest x+y = top-left
    rect[2] = pts[np.argmax(s)]   # largest  x+y = bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # smallest y-x = top-right
    rect[3] = pts[np.argmax(diff)]  # largest  y-x = bottom-left

    return rect


def four_point_transform(image, pts):
    """
    Perspective-warp the image so the document
    fills the entire output (background removed).
    """

    rect = order_points(pts)

    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    destination = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(
        rect,
        destination
    )

    warped = cv2.warpPerspective(
        image,
        matrix,
        (maxWidth, maxHeight)
    )

    return warped


def find_document_corners(paper_mask, ratio):
    """
    From the binary mask, find the 4 document corners
    and scale them back to original image coordinates.
    """

    contours, _ = cv2.findContours(
        paper_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None

    largest = max(contours, key=cv2.contourArea)

    hull = cv2.convexHull(largest)

    perimeter = cv2.arcLength(hull, True)

    # Retry with relaxed epsilon until exactly 4 corners
    for epsilon_factor in [0.02, 0.03, 0.04, 0.05, 0.08, 0.10]:

        approx = cv2.approxPolyDP(
            hull,
            epsilon_factor * perimeter,
            True
        )

        if len(approx) == 4:
            corners = approx.reshape(4, 2).astype("float32")
            corners *= ratio
            return corners

    # Fallback: bounding rectangle corners
    x, y, w, h = cv2.boundingRect(largest)

    corners = np.array([
        [x,     y    ],
        [x + w, y    ],
        [x + w, y + h],
        [x,     y + h]
    ], dtype="float32") * ratio

    return corners


def is_flat_document(image):
    """
    Detect whether an image is already a flat/digital
    document (no real-world background).

    Criteria: the image borders are mostly uniform in
    color (white, light grey, or solid) — typical of
    screenshots, scanned PDFs, and digital certificates.

    Returns True if the image appears to have no
    physical background that needs to be removed.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape

    border_thickness = max(10, min(h, w) // 40)

    # Sample all 4 edges of the image
    top    = gray[:border_thickness, :]
    bottom = gray[h - border_thickness:, :]
    left   = gray[:, :border_thickness]
    right  = gray[:, w - border_thickness:]

    borders = np.concatenate([
        top.flatten(),
        bottom.flatten(),
        left.flatten(),
        right.flatten()
    ])

    mean_val  = np.mean(borders)
    std_val   = np.std(borders)

    # Flat document borders are bright (>180) and
    # very uniform (std < 20) — no noisy background
    is_bright   = mean_val > 180
    is_uniform  = std_val < 20

    return is_bright and is_uniform


def scan_document(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise Exception("Image not found: " + image_path)

    original = image.copy()

    # ------------------------------------
    # Check if image is already a flat /
    # digital document (no background).
    # If so, skip edge detection entirely
    # and return the image as-is for
    # enhancement only.
    # ------------------------------------

    if is_flat_document(image):

        # Return a dummy filtered/mask so
        # the caller signature stays the same
        gray_dummy = cv2.cvtColor(
            cv2.resize(image, (500, 500)),
            cv2.COLOR_BGR2GRAY
        )

        mask_dummy = np.ones(
            gray_dummy.shape,
            dtype=np.uint8
        ) * 255

        # Upscale slightly for consistency
        warped = cv2.resize(
            image,
            None,
            fx=1.5,
            fy=1.5,
            interpolation=cv2.INTER_CUBIC
        )

        return (
            original,
            gray_dummy,
            mask_dummy,
            warped
        )

    # ------------------------------------
    # Physical document: resize for
    # processing (800px gives Canny
    # enough detail)
    # ------------------------------------

    target_height = 800

    ratio = image.shape[0] / target_height

    target_width = int(image.shape[1] / ratio)

    resized = cv2.resize(
        image,
        (target_width, target_height)
    )

    gray = cv2.cvtColor(
        resized,
        cv2.COLOR_BGR2GRAY
    )

    # ------------------------------------
    # Detect document boundary
    # ------------------------------------

    filtered, paper_mask = detect_document(gray)

    if paper_mask is None:
        raise Exception(
            "Could not detect a document in the image. "
            "Ensure the document has visible edges and is "
            "placed on a contrasting background."
        )

    # ------------------------------------
    # Find the 4 document corners
    # ------------------------------------

    corners = find_document_corners(paper_mask, ratio)

    if corners is None:
        raise Exception(
            "Could not locate document corners."
        )

    # ------------------------------------
    # Perspective correction — background
    # is fully removed, output is ONLY
    # the flat document region
    # ------------------------------------

    warped = four_point_transform(original, corners)

    # Upscale for better readability / OCR
    warped = cv2.resize(
        warped,
        None,
        fx=1.5,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    return (
        original,
        filtered,
        paper_mask,
        warped
    )