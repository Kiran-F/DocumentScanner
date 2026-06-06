import img2pdf
from PIL import Image


def export_pdf(image_path, pdf_path):

    image = Image.open(image_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    temp_image = "temp_scan.jpg"

    image.save(temp_image)

    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(
            img2pdf.convert(temp_image)
        )