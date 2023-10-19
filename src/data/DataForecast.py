# type: ignore
import os
import pandas as pd
import numpy as np
from ..entities.S3 import S3
from ..entities.Helper import Helper

class DataForecast:
    def __init__(self):
        self._csv_classes: pd.DataFrame = pd.DataFrame()
        self._csv_descriptions: pd.DataFrame = pd.DataFrame()
        self._program_list = ['30minexpress', 'advanced', 'armsabs', 'beginner', 'bunsabs', 'bunsguns', 'training', 'foundations', 'fullbody']
        self._days_of_the_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        self._s3 = S3()
        self._helper = Helper()
        # data
        self._s3_tblclasses_prefix = 'unloaded-from-snowflake/tblclasses'
        self._s3_tblclassdescriptions_prefix = 'unloaded-from-snowflake/join_tblclasses_tblclassdescriptions'
    
    def _clean_raw_files(self):
        for item in os.listdir('data/raw'):
            item_path = os.path.join('data/raw', item)
            if os.path.isfile(item_path):
                try:
                    os.remove(item_path)  # delete the file
                except Exception as e:
                    print(f"Error deleting {item_path}: {e}")

    def _download(self):
        bucket_name = os.getenv('AWS_S3_BUCKET_DATALAKE')
        data_list = [
            self._s3_tblclasses_prefix,
            self._s3_tblclassdescriptions_prefix
        ]
        for data in data_list:
            response = self._s3.get_files(bucket_name, data)
            for obj in response.get('Contents', []):
                local_file_path = 'data/raw/' + obj['Key'].replace('/', '_')
                self._s3.download_file(bucket_name, obj['Key'], local_file_path)
                if (local_file_path.endswith('gz')):
                    self._helper.uncompress_gz(local_file_path, local_file_path + '.csv')
                    self._helper.delete_file(local_file_path)
            self._helper.merge_csv_files(
                folder_path = 'data/raw',
                file_prefix = data.replace('/', '_')
            )

    def _is_processed(self):
        return (
            self._helper.is_file_present('data/processed', 'class_description.csv') and
            self._helper.is_file_present('data/processed', 'demand.csv')
        )

    def _read(self):
        self._csv_classes = pd.read_csv(
            'data/raw/' + self._s3_tblclasses_prefix.replace('/', '_') + '.csv',
            names = ["CLASSSTARTTIME","CLASSENDTIME","CLASSDATESTART","CLASSDATEEND","CLASSUPDATED","CREATIONDATETIME","LASTMODIFIEDON","CREATEDDATETIMEUTC","MODIFIEDDATETIMEUTC","STUDIOID","CLASSID","SUBCLASSID","DESCRIPTIONID","CLASSTRAINERID","LOCATIONID","PAYSCALEID","CLASSCAPACITY","MAXCAPACITY","TRAINERID2","TRAINERID3","WAITLISTSIZE","EMPID","COURSEID","SEMESTERID","ENROLLEDRESERVED","DROPINRESERVED","CREATEDBY","LASTMODIFIEDBY","BATCHKEY","DAYSUNDAY","DAYMONDAY","DAYTUESDAY","DAYWEDNESDAY","DAYTHURSDAY","DAYFRIDAY","DAYSATURDAY","CLASSACTIVE","NOLOC","FREE","PMTPLAN","USELEADFOLLOWSPLIT","MASKTRAINER","ALLOWUNPAIDS","ALLOWOPENENROLLMENT","TRPAYSASST1","TRPAYSASST2","ALLOWDATEFORWARDENROLLMENT","RECURRING","SOFTDELETED","LOADEDDATETIMEUTC"],
            usecols = ['CLASSDATESTART', 'LOCATIONID', 'CLASSID', 'STUDIOID', 'CLASSTRAINERID', 'CLASSCAPACITY', 'WAITLISTSIZE', 'DAYSUNDAY', 'DAYMONDAY', 'DAYTUESDAY', 'DAYWEDNESDAY', 'DAYTHURSDAY', 'DAYFRIDAY', 'DAYSATURDAY'],
            index_col = False
        )
        self._csv_descriptions = pd.read_csv(
            'data/raw/' + self._csv_descriptions.replace('/', '_') + '.csv', 
            usecols = ['CLASSID', 'CLASSNAME']
        )

    def _preprocess_class_description(self):
        # rename columns
        self._csv_descriptions.rename(
            columns = {
                'CLASSID': 'classid',
                'CLASSNAME': 'classname',
            },
            inplace = True
        )
        # lower case all
        self._csv_descriptions['classname'] = self._csv_descriptions['classname'].str.lower()
        # remove all spaces
        self._csv_descriptions['classname'] = self._csv_descriptions['classname'].str.replace(r'\s', '', case = False, regex = True)
        # remove all symbols
        self._csv_descriptions['classname'] = self._csv_descriptions['classname'].str.replace(r'[^\w\s]', '', case = False, regex = True)
        # remove 'and' word
        self._csv_descriptions['classname'] = self._csv_descriptions['classname'].str.replace(r'and', '', case = False, regex = False)
        # if classname has substring of 'fullbody', replace as 'fullbody' only
        self._csv_descriptions.loc[self._csv_descriptions['classname'].str.contains('fullbody', case = False), 'classname'] = 'fullbody'
        # if classname has substring of 'express', replace as '30minexpress' only
        self._csv_descriptions.loc[self._csv_descriptions['classname'].str.contains('express', case = False), 'classname'] = '30minexpress'
        # if classname has substring of 'foundation', replace as 'foundations' only
        self._csv_descriptions.loc[self._csv_descriptions['classname'].str.contains('foundation', case = False), 'classname'] = 'foundations'
        # if classname has substring of 'advance', replace as 'advanced' only
        self._csv_descriptions.loc[self._csv_descriptions['classname'].str.contains('advance', case = False), 'classname'] = 'advanced'
        # if classname has substring of 'beginner', replace as 'beginner' only
        self._csv_descriptions.loc[self._csv_descriptions['classname'].str.contains('beginner', case = False), 'classname'] = 'beginner'
        # if classname has substring of 'armsabs', replace as 'armsabs' only
        self._csv_descriptions.loc[self._csv_descriptions['classname'].str.contains('armsabs', case = False), 'classname'] = 'armsabs'
        # if classname has substring of 'bunsabs', replace as 'bunsabs' only
        self._csv_descriptions.loc[self._csv_descriptions['classname'].str.contains('bunsabs', case = False), 'classname'] = 'bunsabs'
        # if classname has substring of 'bunsguns', replace as 'bunsguns' only
        self._csv_descriptions.loc[self._csv_descriptions['classname'].str.contains('bunsguns', case = False), 'classname'] = 'bunsguns'
        # if classname has substring of 'training', replace as 'training' only
        self._csv_descriptions.loc[self._csv_descriptions['classname'].str.contains('training', case = False), 'classname'] = 'training'
        # if classname is not one of the allowed values, change to NaN
        self._csv_descriptions.loc[~self._csv_descriptions['classname'].isin(['30minexpress', 'advanced', 'armsabs', 'beginner', 'bunsabs', 'bunsguns', 'training', 'foundations', 'fullbody']), 'classname'] = np.nan
        # save
        np.savetxt('data/processed/class_description.csv', self._csv_descriptions, delimiter=',', header='classid,classname', fmt='%s', comments='')

    def _preprocess_demand(self):
        # rename the selected columns
        self._csv_classes.rename(
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
        self._csv_classes['date'] = pd.to_datetime(self._csv_classes['date'], errors = 'coerce').dt.date
        # clean weekdays
        for col in self._days_of_the_week:
            self._csv_classes[col] = self._csv_classes[col].apply(lambda x: True if str(x).lower() == 'true' else (False if str(x).lower() == 'false' else None))
        self._csv_classes = self._csv_classes.dropna(subset = self._days_of_the_week)
        # aggregate days in single column called day
        self._csv_classes['day'] = None
        for ind, day in enumerate(self._days_of_the_week):
            self._csv_classes.loc[self._csv_classes[day], 'day'] = ind + 1
        self._csv_classes.drop(columns = self._days_of_the_week, inplace = True)
        # add program column
        self._csv_classes = self._csv_classes.merge(pd.read_csv('data/processed/class_description.csv'), on = 'classid', how = 'left')
        self._csv_classes.rename(
            columns = { 'classname': 'program' },
            inplace = True
        )
        # create demand column
        self._csv_classes['demand'] = self._csv_classes['capacity'] + self._csv_classes['waitlist']
        self._csv_classes.drop(columns=['capacity', 'waitlist'], inplace = True)
        # location should be an integer
        self._csv_classes['location'] = self._csv_classes['location'].replace([np.inf, -np.inf], np.nan)
        self._csv_classes = self._csv_classes.dropna()
        self._csv_classes['location'] = self._csv_classes['location'].astype(int)
        # studio should be an integer
        self._csv_classes['studio'] = self._csv_classes['studio'].astype(int)
        # drop coach for now (not part of the independent variable)
        self._csv_classes.drop(columns = ['coach'], inplace = True)
        # remove rows with NA
        self._csv_classes = self._csv_classes.dropna()
        # rearrange columns
        self._csv_classes = self._csv_classes[['date', 'studio', 'location', 'program', 'day', 'demand']]
        # get unique locations and unique programs
        locations = self._csv_classes['location'].unique()
        programs = self._csv_classes['program'].unique()
        # create dataframe for processed data
        data_processed = pd.DataFrame()
        # aggregate rows by date and group by program-location pair
        for loc in locations:
            for prog in programs:
                # filter data by location and program
                data_temp = self._csv_classes[self._csv_classes['location'] == loc]
                data_temp = data_temp[data_temp['program'] == prog]
                # group by the 'date' column and calculate the average of 'demand'
                data_temp = data_temp.groupby('date').agg({
                    'studio': 'first',  # agregate by taking the first value
                    'location': 'first',  # agregate by taking the first value
                    'program': 'first',  # agregate by taking the first value
                    'day': 'first',  # agregate by taking the first value
                    'demand': 'mean'  # agregate by taking the mean
                }).reset_index()
                # create new column called group
                data_temp['group'] = f'{prog}-{loc}'
                # sort rows by date
                data_temp = data_temp.sort_values(by = 'date')
                # concatenate current data group to main processed data
                data_processed = pd.concat([data_processed, data_temp], ignore_index = True)
        # save processed data
        np.savetxt(
            'data/processed/demand.csv',
            data_processed,
            delimiter = ',',
            header = 'date,studio,location,program,day,demand,group',
            fmt = '%s',
            comments = ''
        )

    def preprocess(self, force_fetch: bool):
        if force_fetch or self._is_processed() == False:
            # download raw data
            self._clean_raw_files()
            self._download()
            # read data
            self._read()
            # preprocess
            self._preprocess_class_description()
            self._preprocess_demand()
