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

    def _download(self):
        bucket_name = os.getenv('AWS_S3_BUCKET_DATALAKE')
        #tblclasses
        response = self._s3.get_files(bucket_name, 'unloaded-from-snowflake/tblclasses')
        for obj in response.get('Contents', []):
            local_file_path = 'data/raw/' + obj['Key'].replace('/', '_')
            self._s3.download_file(bucket_name, obj['Key'], local_file_path)
            self._helper.uncompress_gz(local_file_path, local_file_path + '.csv')
            self._helper.delete_file(local_file_path)
        directory = 'data/raw'
        output_filename = 'unloaded-from-snowflake_tblclasses.csv'
        # list all files in the directory
        files = os.listdir(directory)
        # filter files with the prefix and end with '.csv'
        csv_files = [file for file in files if file.startswith('unloaded-from-snowflake_tblclasses') and file.endswith('.csv')]
        # initialize an empty list to store individual data frames
        dfs = []
        # read and merge each CSV file into a data frame
        for csv_file in csv_files:
            df = pd.read_csv(os.path.join(directory, csv_file))
            dfs.append(df)
        # merge all data frames into one
        merged_df = pd.concat(dfs, ignore_index = True)
        # save the merged data frame to a single CSV file
        merged_df.to_csv(os.path.join(directory, output_filename), index=False)
        # delete the individual CSV files (except the merged one)
        for csv_file in csv_files:
            file_path = os.path.join(directory, csv_file)
            if csv_file != output_filename:
                os.remove(file_path)
        # Download from S3 tblclasses_descriptions.csv and saved to data/raw/tblclasses_descriptions.csv

    def _is_processed(self):
        return (
            self._helper.is_file_present('data/processed', 'class_description.csv') and
            self._helper.is_file_present('data/processed', 'demand.csv')
        )

    def _read(self):
        self._csv_classes = pd.read_csv(
            'data/raw/tblclasses_2023-08.csv',
            names = ["CLASSSTARTTIME","CLASSENDTIME","CLASSDATESTART","CLASSDATEEND","CLASSUPDATED","CREATIONDATETIME","LASTMODIFIEDON","CREATEDDATETIMEUTC","MODIFIEDDATETIMEUTC","STUDIOID","CLASSID","SUBCLASSID","DESCRIPTIONID","CLASSTRAINERID","LOCATIONID","PAYSCALEID","CLASSCAPACITY","MAXCAPACITY","TRAINERID2","TRAINERID3","WAITLISTSIZE","EMPID","COURSEID","SEMESTERID","ENROLLEDRESERVED","DROPINRESERVED","CREATEDBY","LASTMODIFIEDBY","BATCHKEY","DAYSUNDAY","DAYMONDAY","DAYTUESDAY","DAYWEDNESDAY","DAYTHURSDAY","DAYFRIDAY","DAYSATURDAY","CLASSACTIVE","NOLOC","FREE","PMTPLAN","USELEADFOLLOWSPLIT","MASKTRAINER","ALLOWUNPAIDS","ALLOWOPENENROLLMENT","TRPAYSASST1","TRPAYSASST2","ALLOWDATEFORWARDENROLLMENT","RECURRING","SOFTDELETED","LOADEDDATETIMEUTC"],
            usecols = ['CLASSDATESTART', 'LOCATIONID', 'CLASSID', 'STUDIOID', 'CLASSTRAINERID', 'CLASSCAPACITY', 'WAITLISTSIZE', 'DAYSUNDAY', 'DAYMONDAY', 'DAYTUESDAY', 'DAYWEDNESDAY', 'DAYTHURSDAY', 'DAYFRIDAY', 'DAYSATURDAY'],
            index_col = False
        )
        self._csv_descriptions = pd.read_csv(
            'data/raw/tblclassdescriptions.csv', 
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
            self._download()
            # read data
            self._read()
            # preprocess
            self._preprocess_class_description()
            self._preprocess_demand()
