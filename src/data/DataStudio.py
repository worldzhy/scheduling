# type: ignore
import os
import pandas as pd
import numpy as np
from ..entities.Config import Config
from ..entities.S3 import S3
from ..entities.Helper import Helper
from ..entities.Constant import Constant

class DataStudio:
    def __init__(self):
        self._csv_studio: pd.DataFrame = pd.DataFrame()
        self._s3 = S3()
        self._helper = Helper()
        # data
        self._datalake_bucket = Config.AWS_S3_BUCKET_DATALAKE
        self._studio_prefix = Config.DATALAKE_STUDIO
    
    def _clean_raw_files(self):
        try:
            self._helper.delete_file('data/raw/' + self._studio_prefix.replace('/', '_') + '.csv')
        except:
            # ignore
            pass

    def _download(self):
        self._helper.download_files_as_one(self._datalake_bucket, self._studio_prefix)

    def _is_processed(self):
        return self._helper.is_file_present('data/processed', 'studio.csv')

    def _read(self):
        self._csv_studio = pd.read_csv(
            'data/raw/' + self._studio_prefix.replace('/', '_') + '.csv',
            usecols = ['STUDIOID', 'STUDIONAME'],
            index_col = False
        )

    def _clean(self):
        # rename columns
        self._csv_studio.rename(
            columns = {
                'STUDIOID': 'id',
                'STUDIONAME': 'name',
            },
            inplace = True
        )
        # drop columns with NA
        self._csv_studio = self._csv_studio.dropna()
        self._csv_studio = self._csv_studio[self._csv_studio['id'] > 0]
        # save
        np.savetxt('data/processed/studio.csv', self._csv_studio, delimiter=',', header='id,name', fmt='%s', comments='')

    def preprocess(self, force_fetch: bool):
        if force_fetch or self._is_processed() == False:
            # download raw data
            self._clean_raw_files()
            self._download()
            # read data
            self._read()
            # preprocess
            self._clean()
