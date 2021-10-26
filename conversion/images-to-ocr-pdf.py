"""
Utility to OCR a list of images and output them as one PDF

License: GNU AGPL 3.0
Author: (c) Harald Lieder, harald.lieder@outlook.com
Date: 2021-10-26
"""
import os
import sys

import fitz

if tuple(map(int, fitz.VersionBind.split("."))) < (1, 19, 0):
    raise ValueError("Need at least PyMuPDF v1.19.0")

doc = fitz.open()  # output PDF
img_folder = sys.argv[1]  # example: image folder name provided
dirname = os.path.dirname(img_folder)
img_list = os.listdir(img_folder)  # some list of image filenames
for img in img_list:
    imgfile = os.path.join(dirname, img)
    pix = fitz.Pixmap(imgfile)  # make a pixmap form the image file
    pdfbytes = pix.pdfocr_tobytes(language="eng")  # 1-page PDF with the OCRed image
    imgpdf = fitz.open("pdf", pdfbytes)  # open it as a PDF
    doc.insert_pdf(imgpdf)  # append the image page to output

doc.ez_save("ocr-pdf.pdf")  # save output
