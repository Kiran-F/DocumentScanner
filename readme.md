# Smart Document Scanner using Digital Image Processing

## Project Overview

The **Smart Document Scanner** is a Digital Image Processing (DIP) project that converts images of documents captured using a mobile phone or camera into clean, scanner-like digital copies.

The system automatically detects document boundaries, removes perspective distortion, enhances readability, reduces noise, and allows exporting multiple scanned pages into a single PDF document.

This project is implemented in **Python** using **OpenCV**, **NumPy**, **Tkinter**, and **PIL**, and follows the Digital Image Processing techniques covered in the course assignments.

---

## Objectives

- Detect document boundaries automatically.
- Remove background and isolate the document.
- Correct skew and perspective distortion.
- Improve readability using image enhancement techniques.
- Reduce noise and unwanted artifacts.
- Export scanned pages as images or a combined PDF.
- Provide a user-friendly graphical interface.

---

## Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| OpenCV | Image Processing |
| NumPy | Numerical Computations |
| Tkinter | Graphical User Interface |
| Pillow (PIL) | Image Display |
| img2pdf | PDF Generation |
| Matplotlib | Visualization & Testing |

---

## Digital Image Processing Techniques Used

### 1. Image Preprocessing

- RGB to Grayscale Conversion
- Image Resizing

Purpose:
- Reduce computational complexity.
- Prepare image for further processing.

---

### 2. Noise Reduction

Implemented using:

- Median Filtering

Purpose:
- Remove impulse noise.
- Preserve edges better than averaging filters.

---

### 3. Edge Detection

Implemented using:

- Canny Edge Detector

Purpose:
- Detect document boundaries.
- Highlight significant edges.

---

### 4. Segmentation and Contour Detection

Implemented using:

- Binary Thresholding
- Contour Extraction
- Convex Hull Generation

Purpose:
- Identify the document region.
- Separate document from background.

---

### 5. Geometric Transformation

Implemented using:

- Perspective Transformation
- Homography Mapping
- Four Point Transform

Purpose:
- Correct perspective distortion.
- Obtain a top-down view of the document.

---

### 6. Image Enhancement

Implemented using:

- Contrast Stretching
- Adaptive Thresholding
- Unsharp Masking

Purpose:
- Improve text visibility.
- Create scanner-like output.

---

### 7. Morphological Operations

Implemented using:

- Dilation
- Erosion
- Opening
- Closing

Purpose:
- Remove small artifacts.
- Strengthen document boundaries.
- Improve segmentation accuracy.

---

## Project Structure

```text
SmartDocumentScanner/
│
├── images/
│   └── sample.jpeg
│
├── scanner.py
├── document_detector.py
├── enhancement.py
├── gui.py
├── main.py
│
├── requirements.txt
└── README.md
```

---

## System Workflow

```text
Input Image
      │
      ▼
Preprocessing
(Grayscale + Resize)
      │
      ▼
Noise Reduction
(Median Filtering)
      │
      ▼
Edge Detection
(Canny)
      │
      ▼
Document Detection
(Contours + Convex Hull)
      │
      ▼
Perspective Correction
(Homography)
      │
      ▼
Image Enhancement
(Thresholding + Contrast Stretching)
      │
      ▼
Scanned Output
      │
      ▼
Save Image / Export PDF
```

---

## Installation

### Step 1: Clone or Download Project

```bash
git clone <repository-url>
```

or download the project folder.

---

### Step 2: Open in VS Code

Open the project folder in VS Code.

---

### Step 3: Create Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

### Step 4: Install Dependencies

```bash
pip install opencv-python
pip install numpy
pip install pillow
pip install matplotlib
pip install img2pdf
```

Or:

```bash
pip install -r requirements.txt
```

---

## Running the Project

### GUI Version

Run:

```bash
python gui.py
```

Features:

- Upload multiple images
- Scan documents
- Navigate between pages
- Save scanned images
- Export multiple pages into a PDF

---

### Testing Version

Run:

```bash
python main.py
```

Displays:

- Original Image
- Preprocessed Image
- Document Detection Stage
- Final Scanned Output

---

## How to Use

### Upload Images

Click:

```text
Upload Images
```

Select one or more document images.

---

### Scan Documents

Click:

```text
Scan Documents
```

The system will:

- Detect document boundaries
- Correct perspective
- Enhance readability
- Generate scanned output

---

### Save Individual Page

Click:

```text
Save Page
```

Save current scanned page as:

- PNG
- JPG

---

### Export PDF

Click:

```text
Export PDF
```

All scanned pages will be combined into a single PDF file.

---

## Features

- Automatic document detection
- Perspective correction
- Noise reduction
- Contrast enhancement
- Adaptive thresholding
- Multiple image support
- PDF generation
- Simple graphical interface
- Fully based on Digital Image Processing techniques
- No machine learning required

---

## Applications

- Assignment digitization
- Lecture notes scanning
- Book page scanning
- Receipt digitization
- Office document archiving
- Educational document management

---

## Future Improvements

- Real-time webcam scanning
- Automatic shadow removal
- OCR integration
- Color document mode
- Auto-rotation correction
- Mobile application deployment
- Batch processing improvements

---

## Conclusion

The Smart Document Scanner demonstrates the practical application of Digital Image Processing techniques including image preprocessing, noise reduction, edge detection, segmentation, geometric transformation, morphological operations, and image enhancement.

The system successfully converts ordinary camera-captured document images into clear, scanner-quality outputs while maintaining a simple and user-friendly interface.