import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
    config=Config(signature_version='s3v4')
)

# Пытаемся создать bucket, но игнорируем ошибку "уже существует"
try:
    s3.create_bucket(Bucket='ml-models')
    print("Bucket создан")
except ClientError as e:
    if 'BucketAlreadyOwnedByYou' in str(e):
        print("Bucket уже существует, продолжаем")
    else:
        raise

# Загружаем модель
s3.upload_file('models/model_v1.pth', 'ml-models', 'model_v1.pth')
print('Модель загружена в S3')
