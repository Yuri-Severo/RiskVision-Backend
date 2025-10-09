import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("AWS_S3_BUCKET")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION,
)

def upload_file_to_s3(file_path: str, key_name: str):
    try:
        s3_client.upload_file(file_path, S3_BUCKET, key_name)
        print(f"✅ Arquivo {file_path} enviado para {S3_BUCKET}/{key_name}")
        return True
    except FileNotFoundError:
        print("❌ Arquivo não encontrado.")
    except NoCredentialsError:
        print("❌ Credenciais AWS não encontradas.")
    except ClientError as e:
        print(f"❌ Erro ao enviar arquivo: {e}")
    return False
