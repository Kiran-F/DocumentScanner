import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

import cv2
import os
import img2pdf

from scanner import scan_document
from enhancement import enhance_document


class SmartScanner:

    def __init__(self, root):

        self.root = root

        self.root.title("Smart Document Scanner")

        self.root.geometry("1200x700")

        self.image_paths = []

        self.scanned_pages = []

        self.current_page = 0

        self.create_widgets()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="SMART DOCUMENT SCANNER",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        btn_frame = tk.Frame(self.root)

        btn_frame.pack()

        upload_btn = tk.Button(
            btn_frame,
            text="Upload Images",
            command=self.upload_image,
            width=15
        )

        upload_btn.grid(row=0, column=0, padx=10)

        scan_btn = tk.Button(
            btn_frame,
            text="Scan Documents",
            command=self.scan_image,
            width=15
        )

        scan_btn.grid(row=0, column=1, padx=10)

        save_btn = tk.Button(
            btn_frame,
            text="Save Page",
            command=self.save_scan,
            width=15
        )

        save_btn.grid(row=0, column=2, padx=10)

        pdf_btn = tk.Button(
            btn_frame,
            text="Export PDF",
            command=self.export_pdf_file,
            width=15
        )

        pdf_btn.grid(row=0, column=3, padx=10)

        prev_btn = tk.Button(
            btn_frame,
            text="◀ Previous",
            command=self.previous_page,
            width=15
        )

        prev_btn.grid(row=0, column=4, padx=10)

        next_btn = tk.Button(
            btn_frame,
            text="Next ▶",
            command=self.next_page,
            width=15
        )

        next_btn.grid(row=0, column=5, padx=10)

        image_frame = tk.Frame(self.root)

        image_frame.pack(pady=20)

        self.left_panel = tk.Label(
            image_frame,
            text="Original Image",
            font=("Arial", 12)
        )

        self.left_panel.grid(
            row=0,
            column=0,
            padx=30
        )

        self.right_panel = tk.Label(
            image_frame,
            text="Scanned Output",
            font=("Arial", 12)
        )

        self.right_panel.grid(
            row=0,
            column=1,
            padx=30
        )

        self.page_label = tk.Label(
            self.root,
            text="Page 0 / 0",
            font=("Arial", 12)
        )

        self.page_label.pack()

        self.status = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 12)
        )

        self.status.pack(
            side="bottom",
            pady=10
        )

    def upload_image(self):

        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png")
            ]
        )

        if not files:
            return

        self.image_paths = list(files)

        image = Image.open(
            self.image_paths[0]
        )

        image.thumbnail((500, 500))

        photo = ImageTk.PhotoImage(image)

        self.left_panel.configure(
            image=photo,
            text=""
        )

        self.left_panel.image = photo

        self.status.config(
            text=f"{len(self.image_paths)} image(s) loaded"
        )

    def scan_image(self):

        if not self.image_paths:

            messagebox.showerror(
                "Error",
                "Please upload image(s) first."
            )

            return

        self.scanned_pages = []

        try:

            for path in self.image_paths:

                original, filtered, mask, scanned = scan_document(
                    path
                )

                final_scan = enhance_document(
                    scanned
                )

                self.scanned_pages.append(
                    final_scan
                )

            self.current_page = 0

            self.show_current_page()

            self.status.config(
                text=f"{len(self.scanned_pages)} page(s) scanned successfully"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def show_current_page(self):

        if not self.scanned_pages:
            return

        image = Image.fromarray(
            self.scanned_pages[self.current_page]
        )

        image.thumbnail((500, 500))

        photo = ImageTk.PhotoImage(image)

        self.right_panel.configure(
            image=photo,
            text=""
        )

        self.right_panel.image = photo

        self.page_label.config(
            text=f"Page {self.current_page + 1} / {len(self.scanned_pages)}"
        )

    def next_page(self):

        if not self.scanned_pages:
            return

        if self.current_page < len(self.scanned_pages) - 1:

            self.current_page += 1

            self.show_current_page()

    def previous_page(self):

        if not self.scanned_pages:
            return

        if self.current_page > 0:

            self.current_page -= 1

            self.show_current_page()

    def save_scan(self):

        if not self.scanned_pages:

            messagebox.showerror(
                "Error",
                "No scanned pages available."
            )

            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg")
            ]
        )

        if path:

            cv2.imwrite(
                path,
                self.scanned_pages[self.current_page]
            )

            self.status.config(
                text="Page saved successfully"
            )

    def export_pdf_file(self):

        if not self.scanned_pages:

            messagebox.showerror(
                "Error",
                "No scanned pages available."
            )

            return

        pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[
                ("PDF File", "*.pdf")
            ]
        )

        if not pdf_path:
            return

        temp_files = []

        try:

            for i, page in enumerate(self.scanned_pages):

                filename = f"temp_page_{i}.jpg"

                cv2.imwrite(
                    filename,
                    page
                )

                temp_files.append(
                    filename
                )

            with open(pdf_path, "wb") as pdf:

                pdf.write(
                    img2pdf.convert(
                        temp_files
                    )
                )

            self.status.config(
                text=f"{len(self.scanned_pages)} pages exported to PDF"
            )

        finally:

            for file in temp_files:

                if os.path.exists(file):

                    os.remove(file)


root = tk.Tk()

app = SmartScanner(root)

root.mainloop()