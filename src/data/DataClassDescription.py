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
            self._helper.delete_file(Constant.PATH_FOLDER_RAW + self._file_prefix.replace('/', '_') + '.csv')
        except:
            # ignore
            pass

    def _download(self):
        self._helper.download_files_as_one(self._bucket, self._file_prefix)

    def _is_downloaded(self):
        return self._helper.is_file_present(Constant.PATH_FOLDER_RAW + self._file_prefix.replace('/', '_') + '.csv')

    def _read(self):
        self._csv = pd.read_csv(
            Constant.PATH_FOLDER_RAW + self._file_prefix.replace('/', '_') + '.csv',
            usecols = ['CLASSID', 'CLASSNAME'],
            index_col = False
        )

    def _clean(self):
        # rename columns
        self._csv.rename(
            columns = {
                'CLASSID': 'id',
                'CLASSNAME': 'program_id',
            },
            inplace = True
        )
        # drop columns with NA
        self._csv = self._csv.dropna()
        # lower case all
        self._csv['program_id'] = self._csv['program_id'].str.lower()
        # remove all spaces
        self._csv['program_id'] = self._csv['program_id'].str.replace(r'\s', '', case = False, regex = True)
        # remove all symbols
        self._csv['program_id'] = self._csv['program_id'].str.replace(r'[^\w\s]', '', case = False, regex = True)
        # remove 'and' word
        self._csv['program_id'] = self._csv['program_id'].str.replace(r'and', '', case = False, regex = False)
        # if classname has substring of 'fullbody', replace as 'fullbody' only
        self._csv.loc[self._csv['program_id'].str.contains('fullbody', case = False), 'program_id'] = 'fullbody'
        # if classname has substring of 'express', replace as '30minexpress' only
        self._csv.loc[self._csv['program_id'].str.contains('express', case = False), 'program_id'] = '30minexpress'
        # if classname has substring of 'foundation', replace as 'foundations' only
        self._csv.loc[self._csv['program_id'].str.contains('foundation', case = False), 'program_id'] = 'foundations'
        # if classname has substring of 'advance', replace as 'advanced' only
        self._csv.loc[self._csv['program_id'].str.contains('advance', case = False), 'program_id'] = 'advanced'
        # if classname has substring of 'beginner', replace as 'beginner' only
        self._csv.loc[self._csv['program_id'].str.contains('beginner', case = False), 'program_id'] = 'beginner'
        # if classname has substring of 'armsabs', replace as 'armsabs' only
        self._csv.loc[self._csv['program_id'].str.contains('armsabs', case = False), 'program_id'] = 'armsabs'
        # if classname has substring of 'bunsabs', replace as 'bunsabs' only
        self._csv.loc[self._csv['program_id'].str.contains('bunsabs', case = False), 'program_id'] = 'bunsabs'
        # if classname has substring of 'bunsguns', replace as 'bunsguns' only
        self._csv.loc[self._csv['program_id'].str.contains('bunsguns', case = False), 'program_id'] = 'bunsguns'
        # if classname has substring of 'training', replace as 'training' only
        self._csv.loc[self._csv['program_id'].str.contains('training', case = False), 'program_id'] = 'training'
        # if classname is not one of the allowed values, change to NaN and drop
        self._csv.loc[~self._csv['program_id'].isin(self._program_list), 'program_id'] = np.nan
        self._csv = self._csv.dropna()
        # use id for program instead of name
        name_mapping = {value: index for index, value in enumerate(self._program_list)}
        self._csv['program_id'] = self._csv['program_id'].replace(name_mapping)
        self._csv['program_id'] = self._csv['program_id'].astype(int)
        # save
        self._csv.to_csv(Constant.PATH_CSV_CLASS_DESC, index=False, quoting=csv.QUOTE_NONNUMERIC)

    def preprocess(self, force_fetch: bool):
        if force_fetch or self._is_downloaded() == False:
            # download raw data
            self._clean_raw_files()
            self._download()
        # read data
        self._read()
        # preprocess
        self._clean()
