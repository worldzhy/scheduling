import os

class Config:
    # App
    APP_DEBUG = os.getenv('APP_DEBUG')
    # S3
    AWS_S3_BUCKET_DATALAKE = os.getenv('AWS_S3_BUCKET_DATALAKE')
    AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID'),
    AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY'),
    AWS_S3_REGION = os.getenv('AWS_S3_REGION')
