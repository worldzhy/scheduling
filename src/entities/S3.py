import os
import boto3

class S3:
    def __init__(self):
        self._s3 = boto3.client('s3',
            aws_access_key_id = os.getenv('AWS_S3_ACCESS_KEY_ID'),
            aws_secret_access_key = os.getenv('AWS_S3_SECRET_ACCESS_KEY'),
            region_name = os.getenv('AWS_S3_REGION')
        )

    def upload_file(self, file_path: str, bucket_name: str, s3_path: str):
        self._s3.upload_file(
            file_path,
            bucket_name,
            s3_path
        )

    def download_file(self, bucket_name: str, s3_path: str, file_path: str):
        self._s3.download_file(
            bucket_name,
            s3_path,
            file_path
        )

    def list_files(self, bucket_name: str):
        response = self._s3.list_objects_v2(Bucket = bucket_name)
        for obj in response.get('Contents', []):
            print(f'Object key: {obj["Key"]}, Size: {obj["Size"]} bytes')

    def copy_file(self, bucket_name: str, current_s3_path: str, new_s3_path: str):
        self._s3.copy_object(
            CopySource = { 'Bucket': bucket_name, 'Key': current_s3_path },
            Bucket = bucket_name,
            Key= new_s3_path
        )

    def delete_file(self, bucket_name: str, s3_path: str):
        self._s3.delete_object(
            Bucket = bucket_name,
            Key = s3_path
        )

    def rename_file(self, bucket_name: str, current_s3_path: str, new_s3_path: str):
        self.copy_file(bucket_name, current_s3_path, new_s3_path)
        self.delete_file(bucket_name, current_s3_path)
