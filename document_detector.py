import cv2
import numpy as np


def detect_document(gray):

    height, width = gray.shape

    # ------------------------------------
    # Median Filter (noise reduction)
    # ------------------------------------

    kernel_size = max(5, width // 60)

    if kernel_size % 2 == 0:
        kernel_size += 1

    filtered = cv2.medianBlur(
        gray,
        kernel_size
    )

    # ------------------------------------
    # Canny Edge Detection
    # Use fixed thresholds — auto (median-
    # based) thresholds fail on bright docs
    # because median ~193 pushes lower
    # threshold too high (127), missing
    # the document border edges.
    # ------------------------------------

    edges = cv2.Canny(
        filtered,
        30,
        100
    )

    # ------------------------------------
    # Dilate edges to close small gaps
    # ------------------------------------

    kernel = np.ones((5, 5), np.uint8)

    edges = cv2.dilate(
        edges,
        kernel,
        iterations=1
    )

    # ------------------------------------
    # Find contours sorted by area
    # ------------------------------------

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return filtered, None

    contours = sorted(
        contours,
        key=cv2.contourArea,
        reverse=True
    )

    image_area = height * width

    # Minimum 10% of image, maximum 88%.
    # The >88% cap filters out the image-
    # border artifact that Canny+dilate
    # creates along the very edge of the
    # frame — its hull covers ~95% of the
    # image and is NOT the document.
    min_area = 0.10 * image_area
    max_area = 0.88 * image_area

    best_mask = None

    for contour in contours:

        hull = cv2.convexHull(contour)

        hull_area = cv2.contourArea(hull)

        if hull_area > max_area:
            continue  # skip image-border artifact

        if hull_area < min_area:
            break     # remaining contours too small

        perimeter = cv2.arcLength(hull, True)

        # Try relaxing epsilon until we get exactly 4 corners
        for epsilon_factor in [0.02, 0.03, 0.04, 0.05, 0.08, 0.10]:

            approx = cv2.approxPolyDP(
                hull,
                epsilon_factor * perimeter,
                True
            )

            if len(approx) == 4:

                mask = np.zeros(
                    (height, width),
                    dtype=np.uint8
                )

                cv2.drawContours(
                    mask,
                    [approx],
                    -1,
                    255,
                    thickness=cv2.FILLED
                )

                best_mask = mask
                break

        if best_mask is not None:
            break

    # ------------------------------------
    # Fallback: use largest valid contour's
    # convex hull if no clean quad found
    # ------------------------------------

    if best_mask is None:

        for contour in contours:

            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)

            if hull_area > max_area:
                continue

            if hull_area < min_area:
                break

            mask = np.zeros(
                (height, width),
                dtype=np.uint8
            )

            cv2.drawContours(
                mask,
                [hull],
                -1,
                255,
                thickness=cv2.FILLED
            )

            best_mask = mask
            break

    return filtered, best_mask
