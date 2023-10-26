# type: ignore
import pandas as pd
import numpy as np
import csv
from ..entities.Config import Config
from ..entities.S3 import S3
from ..entities.Helper import Helper
from ..entities.Constant import Constant

class DataClass:
    def __init__(self):
        self._csv: pd.DataFrame = pd.DataFrame()
        self._s3 = S3()
        self._helper = Helper()
        self._program_list = Constant.PROGRAM_LIST
        self._days_of_the_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        # data
        self._bucket = Config.AWS_S3_BUCKET_DATALAKE
        self._file_prefix = Config.DATALAKE_TBLCLASSES
    
    def _clean_raw_files(self):
        try:
            self._helper.delete_file('data/raw/' + self._file_prefix.replace('/', '_') + '.csv')
        except:
            # ignore
            pass

    def _download(self):
        self._helper.download_files_as_one(self._bucket, self._file_prefix)

    def _is_processed(self):
        return self._helper.is_file_present('data/processed', 'class.csv')

    def _read(self):
        self._csv = pd.read_csv(
            'data/raw/' + self._file_prefix.replace('/', '_') + '.csv',
            names = ["CLASSSTARTTIME","CLASSENDTIME","CLASSDATESTART","CLASSDATEEND","CLASSUPDATED","CREATIONDATETIME","LASTMODIFIEDON","CREATEDDATETIMEUTC","MODIFIEDDATETIMEUTC","STUDIOID","CLASSID","SUBCLASSID","DESCRIPTIONID","CLASSTRAINERID","LOCATIONID","PAYSCALEID","CLASSCAPACITY","MAXCAPACITY","TRAINERID2","TRAINERID3","WAITLISTSIZE","EMPID","COURSEID","SEMESTERID","ENROLLEDRESERVED","DROPINRESERVED","CREATEDBY","LASTMODIFIEDBY","BATCHKEY","DAYSUNDAY","DAYMONDAY","DAYTUESDAY","DAYWEDNESDAY","DAYTHURSDAY","DAYFRIDAY","DAYSATURDAY","CLASSACTIVE","NOLOC","FREE","PMTPLAN","USELEADFOLLOWSPLIT","MASKTRAINER","ALLOWUNPAIDS","ALLOWOPENENROLLMENT","TRPAYSASST1","TRPAYSASST2","ALLOWDATEFORWARDENROLLMENT","RECURRING","SOFTDELETED","LOADEDDATETIMEUTC"],
            usecols = ['CLASSDATESTART', 'LOCATIONID', 'CLASSID', 'STUDIOID', 'CLASSTRAINERID', 'CLASSCAPACITY', 'WAITLISTSIZE', 'DAYSUNDAY', 'DAYMONDAY', 'DAYTUESDAY', 'DAYWEDNESDAY', 'DAYTHURSDAY', 'DAYFRIDAY', 'DAYSATURDAY'],
            index_col = False
        )

    def _clean(self):
        # rename columns
        self._csv.rename(
            columns = {
                'CLASSDATESTART': 'date',
                'LOCATIONID': 'location',
                'CLASSID': 'classid',
                'STUDIOID': 'studio',
                'CLASSTRAINERID': 'coach',
                'CLASSCAPACITY': 'capacity',
                'WAITLISTSIZE': 'waitlist',
                'DAYSUNDAY': 'sunday',
                'DAYMONDAY': 'monday',
                'DAYTUESDAY': 'tuesday',
                'DAYWEDNESDAY': 'wednesday',
                'DAYTHURSDAY': 'thursday',
                'DAYFRIDAY': 'friday',
                'DAYSATURDAY': 'saturday',
            },
            inplace = True
        )
        # convert the date column to datetime
        self._csv['date'] = pd.to_datetime(self._csv['date'], errors = 'coerce').dt.date
        # clean weekdays
        for col in self._days_of_the_week:
            self._csv[col] = self._csv[col].apply(lambda x: True if str(x).lower() == 'true' else (False if str(x).lower() == 'false' else None))
        self._csv = self._csv.dropna(subset = self._days_of_the_week)
        # aggregate days in single column called day
        self._csv['day'] = None
        for ind, day in enumerate(self._days_of_the_week):
            self._csv.loc[self._csv[day], 'day'] = ind + 1
        self._csv.drop(columns = self._days_of_the_week, inplace = True)
        # location should be an integer
        self._csv['location'] = self._csv['location'].replace([np.inf, -np.inf], np.nan)
        self._csv = self._csv.dropna()
        self._csv['location'] = self._csv['location'].astype(int)
        # studio should be an integer
        self._csv['studio'] = self._csv['studio'].astype(int)
        # drop coach for now (not part of the independent variable)
        self._csv.drop(columns = ['coach'], inplace = True)
        # remove rows with NA
        self._csv = self._csv.dropna()
        # rearrange columns
        self._csv = self._csv[['date', 'studio', 'location', 'program', 'day', 'demand']]
        # create new column called group
        self._csv['group'] = self._csv['program'] + '-' + self._csv['location']
        # save processed data
        self._csv.to_csv('data/processed/class.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

    def preprocess(self, force_fetch: bool):
        if force_fetch or self._is_processed() == False:
            # download raw data
            self._clean_raw_files()
            self._download()
            # read data
            self._read()
            # preprocess
            self._clean()
