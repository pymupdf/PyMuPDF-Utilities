import os
import fitz  # pymupdf
from azure.storage.blob import BlobClient

blob = BlobClient.from_connection_string(
    conn_str="my_connection_string",
    container_name="my_container",
    blob_name="my_blob",
)

with open("some-file.pdf", "wb") as my_blob:
    blob_data = blob.download_blob()
    blob_data.readinto(my_blob)

# now open with PyMuPDF using the bytes object of "f"
doc = fitz.open("pdf", my_blob.read())
