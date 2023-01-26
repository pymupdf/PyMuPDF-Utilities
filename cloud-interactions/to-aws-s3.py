import fitz
import boto3

# process some PDF document
doc = fitz.open("...")
# then write / upload it directly to AWS S3
# Instead of save, we use the tobytes(), which generates a bytes object
pdfbytes = doc.tobytes(  # optional 'save' parameters:
    garbage=3,
    deflate=True,
    owner_pw="owner-password",
    user_pw="user-pasword",
)

s3 = boto3.client("s3")
request_route = "string"
request_token = "string"
s3.write_get_object_response(
    Body=pdfbytes,
    RequestRoute=request_route,
    RequestToken=request_token,
)
