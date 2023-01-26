import fitz
import boto3

s3 = boto3.client("s3")

# fill in your credentials to access the cloud
response = s3.get_object(Bucket="string", Key="string")
mime = response["ContentType"]
body = response["Body"]

# define Document with these data
doc = fitz.open(mime, body.read())
