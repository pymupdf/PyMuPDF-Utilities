import fitz  # pymupdf
from azure.storage.blob import BlobClient

# some PDF document
doc = fitz.open("...")

# access Azure blob client
blob = BlobClient.from_connection_string(
    conn_str="my_connection_string",
    container_name="my_container",
    blob_name="my_blob",
)

# upload document
blob.upload_blob(
    doc.tobytes(
        garbage=3,
        deflate=True,
        # more parameters
    )
)
