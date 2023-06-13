# How To Install and Enable Tesseract Dynamically

In some interactive environments, like Google Colab, JupyterLite and other Pyodide-based environments, you have access to a Python environment, that has a set of pre-installed packages. These configurations may not suffice your requirements.

While there are ways to dynamically pip-install packages via invoking pip as a shell command, or even installing software packages in the virtual machine hosting the interactive Python, additional considerations are required for PyMuPDF's OCR support of Tesseract-OCR:

* On importing PyMuPDF, a check is made, whether `os.environ["TESSDATA_PREFIX"]` exists. If yes, its value is stored in `fitz.TESSDATA_PREFIX`, else that value is set to `None`.

* If your notebook requires OCR support, do follow these steps:

    1. `!apt install tesseract-ocr`. When done, confirm the value of Tesseract's language support folder.

    2. `os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata"`

    3. `import fitz`

* You should now be able to use PyMuPDF's OCR functions.