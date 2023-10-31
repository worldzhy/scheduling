# type: ignore
import pandas as pd
import numpy as np
import csv
from ..entities.Config import Config
from ..entities.S3 import S3
from ..entities.Helper import Helper
from ..entities.Constant import Constant

class DataLocation:
    def __init__(self):
        self._csv: pd.DataFrame = pd.DataFrame()
        self._s3 = S3()
        self._helper = Helper()
        # data
        self._bucket = Config.AWS_S3_BUCKET_DATALAKE
        self._file_prefix = Config.DATALAKE_LOCATION
    
    def _clean_raw_files(self):
        try:
            self._helper.delete_file(Constant.PATH_RAW + self._file_prefix.replace('/', '_') + '.csv')
        except:
            # ignore
            pass

    def _download(self):
        self._helper.download_files_as_one(self._bucket, self._file_prefix)

    def _is_processed(self):
        return self._helper.is_file_present(Constant.PATH_PROCESSED + Constant.CSV_LOCATION)

    def _read(self):
        self._csv = pd.read_csv(
            Constant.PATH_RAW + self._file_prefix.replace('/', '_') + '.csv',
            usecols = ['STUDIOID', 'LOCATIONID', 'LOCATIONNAME'],
            index_col = False
        )

    def _clean(self):
        # rename columns
        self._csv.rename(
            columns = {
                'STUDIOID': 'studio_id',
                'LOCATIONID': 'id',
                'LOCATIONNAME': 'name',
            },
            inplace = True
        )
        # drop columns with NA
        self._csv = self._csv.dropna()
        self._csv = self._csv[self._csv['id'] > 0]
        # save
        self._csv.to_csv(Constant.PATH_PROCESSED + Constant.CSV_LOCATION, index=False, quoting=csv.QUOTE_NONNUMERIC)

    def preprocess(self, force_fetch: bool):
        if force_fetch or self._is_processed() == False:
            # download raw data
            self._clean_raw_files()
            self._download()
            # read data
            self._read()
            # preprocess
            self._clean()
