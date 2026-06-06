import cv2
import matplotlib.pyplot as plt

from scanner import scan_document
from enhancement import enhance_document


IMAGE_PATH = "images/sample.jpeg"


try:
    # original, edges, scanned = scan_document(
    #     IMAGE_PATH
    # )
    
    original, filtered, paper_mask, scanned = scan_document(
        IMAGE_PATH
    )

    final_scan = enhance_document(
        scanned
    )
    
    plt.figure(figsize=(16,8))

    plt.subplot(2,2,1)
    plt.imshow(
        cv2.cvtColor(
            original,
            cv2.COLOR_BGR2RGB
        )
    )
    plt.title("Original")
    plt.axis("off")

    plt.subplot(2,2,2)
    plt.imshow(
        filtered,
        cmap="gray"
    )
    plt.title("Median Filter")
    plt.axis("off")

    plt.subplot(2,2,3)
    plt.imshow(
        paper_mask,
        cmap="gray"
    )
    plt.title("Detected Page Mask")
    plt.axis("off")

    plt.subplot(2,2,4)
    plt.imshow(
        final_scan,
        cmap="gray"
    )
    plt.title("Final Scan")
    plt.axis("off")

    plt.tight_layout()
    plt.show()
    
    
    
except Exception as e:

    print("\nERROR:")
    print(e)