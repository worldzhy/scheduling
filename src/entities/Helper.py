import gzip
import os

class Helper:
    def uncompress_gz(self, gz_file_path: str, output_file_path: str):
        # Open the .gz file for reading
        with gzip.open(gz_file_path, 'rb') as f_in:
            # Read the compressed data
            compressed_data = f_in.read()

        # Open the new file for writing
        with open(output_file_path, 'wb') as f_out:
            # Write the uncompressed data to the new file
            f_out.write(compressed_data)

    def is_file_present(self, folder_path: str, file_name: str):
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            return True
        else:
            return False