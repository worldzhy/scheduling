import gzip
import os
import shutil
from .Constant import Constant
from .S3 import S3

class Helper:
    def __init__(self):
        self._s3 = S3()

    def uncompress_gz(self, gz_file_path: str, output_file_path: str):
        # open the .gz file for reading
        with gzip.open(gz_file_path, 'rb') as f_in:
            # read the compressed data
            compressed_data = f_in.read()
        # open the new file for writing
        with open(output_file_path, 'wb') as f_out:
            # write the uncompressed data to the new file
            f_out.write(compressed_data)

    def is_file_present(self, file_path: str):
        if os.path.exists(file_path):
            return True
        else:
            return False
        
    def delete_file(self, file_path: str):
        os.remove(file_path)

    def rename_file(self, old_file_path: str, new_file_path: str):
        try:
            os.rename(old_file_path, new_file_path)
        except FileNotFoundError:
            raise Exception(f'Error: The file "{old_file_path}" does not exist.')

    def merge_csv_files(self, folder_path: str, file_prefix: str):
        # prepare filename of merged file
        merged_filename = file_prefix + '.csv'
        # list all files in the directory
        files = os.listdir(folder_path)
        # filter files with the prefix and end with '.csv'
        csv_files = [file for file in files if file.startswith(file_prefix) and file.endswith('.csv')]
        # read and merge each CSV file into a data frame
        with open(os.path.join(folder_path, merged_filename), 'wb') as outfile:
            for csv_file in csv_files:
                with open(os.path.join(folder_path, csv_file), 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)
                outfile.write(b'\n')
        # delete the individual CSV files (except the merged one)
        for csv_file in csv_files:
            file_path = os.path.join(folder_path, csv_file)
            if csv_file != merged_filename:
                os.remove(file_path)

    def download_files_as_one(self, bucket_name: str, s3_prefix: str):
        response = self._s3.get_files(bucket_name, s3_prefix)
        for obj in response.get('Contents', []):
            local_file_path = Constant.PATH_FOLDER_RAW + obj['Key'].replace('/', '_')
            self._s3.download_file(bucket_name, obj['Key'], local_file_path)
            if (local_file_path.endswith('gz')):
                self.uncompress_gz(local_file_path, local_file_path + '.csv')
                self.delete_file(local_file_path)
        self.merge_csv_files(
            folder_path = Constant.PATH_FOLDER_RAW,
            file_prefix = s3_prefix.replace('/', '_')
        )