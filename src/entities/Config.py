import os

def get_env(env_name: str) -> str:
        val = os.getenv(env_name)
        if (val is None):
            raise Exception(f'Environment variable {env_name} not found.')
        return val

class Config:
    # App
    APP_DEBUG = get_env('APP_DEBUG')
    # S3
    AWS_S3_BUCKET_DATALAKE = get_env('AWS_S3_BUCKET_DATALAKE')
    AWS_S3_ACCESS_KEY_ID = get_env('AWS_S3_ACCESS_KEY_ID'),
    AWS_S3_SECRET_ACCESS_KEY = get_env('AWS_S3_SECRET_ACCESS_KEY'),
    AWS_S3_REGION = get_env('AWS_S3_REGION')
    