import gzip
import os
import pandas as pd

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
        
    def delete_file(self, file_path: str):
        os.remove(file_path)

    def merge_csv_files(self, folder_path: str, file_prefix: str):
        # prepare filename of merged file
        merged_filename = file_prefix + '.csv'
        # list all files in the directory
        files = os.listdir(folder_path)
        # filter files with the prefix and end with '.csv'
        csv_files = [file for file in files if file.startswith(file_prefix) and file.endswith('.csv')]
        # initialize an empty list to store individual data frames
        dfs = []
        # read and merge each CSV file into a data frame
        for csv_file in csv_files:
            df = pd.read_csv(os.path.join(folder_path, csv_file))
            dfs.append(df)
        # merge all data frames into one
        merged_df = pd.concat(dfs, ignore_index = True)
        # save the merged data frame to a single CSV file
        merged_df.to_csv(os.path.join(folder_path, merged_filename), index=False)
        # delete the individual CSV files (except the merged one)
        for csv_file in csv_files:
            file_path = os.path.join(folder_path, csv_file)
            if csv_file != merged_filename:
                os.remove(file_path)