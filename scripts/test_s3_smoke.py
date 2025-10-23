import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

load_dotenv()

bucket = os.environ["AWS_S3_BUCKET"]
region = os.environ["AWS_REGION"]

s3 = boto3.client(
    "s3",
    region_name=region,
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL")
)

# 1) HEAD do bucket
s3.head_bucket(Bucket=bucket)
print("✅ Consegui acessar o bucket:", bucket)

# 2) Upload de um objeto pequeno em memória
key = "health/test.txt"
s3.put_object(Bucket=bucket, Key=key, Body=b"hello s3")
print("✅ Upload OK:", key)

# 3) Listar para conferir
resp = s3.list_objects_v2(Bucket=bucket, Prefix="health/")
print("📦 Objetos:", [o["Key"] for o in resp.get("Contents", [])])
