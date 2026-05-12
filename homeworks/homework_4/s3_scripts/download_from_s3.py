import boto3
from botocore.client import Config

# Подключение к MinIO
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
    config=Config(signature_version='s3v4')
)

# Скачиваем модель
s3.download_file('ml-models', 'model_v1.pth', 'models/model_v1_pretrained.pth')

print('Модель скачана из S3 в models/model_v1_pretrained.pth')
