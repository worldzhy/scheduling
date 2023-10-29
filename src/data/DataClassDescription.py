# type: ignore
import pandas as pd
import numpy as np
import csv
from ..entities.Config import Config
from ..entities.S3 import S3
from ..entities.Helper import Helper
from ..entities.Constant import Constant

class DataClassDesc:
    def __init__(self):
        self._csv: pd.DataFrame = pd.DataFrame()
        self._s3 = S3()
        self._helper = Helper()
        self._program_list = Constant.PROGRAM_LIST
        # data
        self._bucket = Config.AWS_S3_BUCKET_DATALAKE
        self._file_prefix = Config.DATALAKE_TBLCLASSDESCRIPTIONS
    
    def _clean_raw_files(self):
        try:
            self._helper.delete_file('data/raw/' + self._file_prefix.replace('/', '_') + '.csv')
        except:
            # ignore
            pass

    def _download(self):
        self._helper.download_files_as_one(self._bucket, self._file_prefix)

    def _is_processed(self):
        return self._helper.is_file_present('data/processed', 'class_description.csv')

    def _read(self):
        self._csv = pd.read_csv(
            'data/raw/' + self._file_prefix.replace('/', '_') + '.csv',
            usecols = ['CLASSID', 'CLASSNAME'],
            index_col = False
        )

    def _clean(self):
        # rename columns
        self._csv.rename(
            columns = {
                'CLASSID': 'id',
                'CLASSNAME': 'name',
            },
            inplace = True
        )
        # drop columns with NA
        self._csv = self._csv.dropna()
        # lower case all
        self._csv['name'] = self._csv['name'].str.lower()
        # remove all spaces
        self._csv['name'] = self._csv['name'].str.replace(r'\s', '', case = False, regex = True)
        # remove all symbols
        self._csv['name'] = self._csv['name'].str.replace(r'[^\w\s]', '', case = False, regex = True)
        # remove 'and' word
        self._csv['name'] = self._csv['name'].str.replace(r'and', '', case = False, regex = False)
        # if classname has substring of 'fullbody', replace as 'fullbody' only
        self._csv.loc[self._csv['name'].str.contains('fullbody', case = False), 'name'] = 'fullbody'
        # if classname has substring of 'express', replace as '30minexpress' only
        self._csv.loc[self._csv['name'].str.contains('express', case = False), 'name'] = '30minexpress'
        # if classname has substring of 'foundation', replace as 'foundations' only
        self._csv.loc[self._csv['name'].str.contains('foundation', case = False), 'name'] = 'foundations'
        # if classname has substring of 'advance', replace as 'advanced' only
        self._csv.loc[self._csv['name'].str.contains('advance', case = False), 'name'] = 'advanced'
        # if classname has substring of 'beginner', replace as 'beginner' only
        self._csv.loc[self._csv['name'].str.contains('beginner', case = False), 'name'] = 'beginner'
        # if classname has substring of 'armsabs', replace as 'armsabs' only
        self._csv.loc[self._csv['name'].str.contains('armsabs', case = False), 'name'] = 'armsabs'
        # if classname has substring of 'bunsabs', replace as 'bunsabs' only
        self._csv.loc[self._csv['name'].str.contains('bunsabs', case = False), 'name'] = 'bunsabs'
        # if classname has substring of 'bunsguns', replace as 'bunsguns' only
        self._csv.loc[self._csv['name'].str.contains('bunsguns', case = False), 'name'] = 'bunsguns'
        # if classname has substring of 'training', replace as 'training' only
        self._csv.loc[self._csv['name'].str.contains('training', case = False), 'name'] = 'training'
        # if classname is not one of the allowed values, change to NaN and drop
        self._csv.loc[~self._csv['name'].isin(self._program_list), 'name'] = np.nan
        self._csv = self._csv.dropna()
        # use id for program instead of name
        name_mapping = {value: index for index, value in enumerate(self._program_list)}
        self._csv['name'] = self._csv['name'].replace(name_mapping)
        self._csv['name'] = self._csv['name'].astype(int)
        # save
        self._csv.to_csv('data/processed/class_description.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

    def preprocess(self, force_fetch: bool):
        if force_fetch or self._is_processed() == False:
            # download raw data
            self._clean_raw_files()
            self._download()
            # read data
            self._read()
            # preprocess
            self._clean()
