# type: ignore
import pandas as pd
import csv

from ..entities.Constant import Constant
from ..data.DataClassV2 import DataClass as DataClassV2
from ..data.DataClassDescription import DataClassDesc
from ..entities.Helper import Helper

class DataDemand:
    def __init__(self, start_time: str, end_time: str):
        self._class_csv: pd.DataFrame = pd.DataFrame()
        self._class_desc_csv: pd.DataFrame = pd.DataFrame()
        self._helper = Helper()
        # inputs
        self._start_time = start_time
        self._end_time = end_time
        # data
        self._class_file_prefix = 'class'
        self._class_desc_file_prefix = 'class_description'
        # data dependencies
        self._data_class = DataClassV2()
        self._data_class_desc = DataClassDesc()

    
    def _clean_raw_files(self):
        try:
            file_prefixes = [
                self._class_file_prefix,
                self._class_desc_file_prefix
            ]
            for file_prefix in file_prefixes:
                self._helper.delete_file(Constant.PATH_FOLDER_PROCESSED + file_prefix.replace('/', '_') + '.csv')
        except:
            # ignore
            pass

    def _download(self):
        self._data_class.preprocess(force_fetch=True)
        self._data_class_desc.preprocess(force_fetch=True)

    def _is_processed(self):
        return self._helper.is_file_present(Constant.PATH_CSV_DEMAND)

    def _read(self):
        self._class_csv = pd.read_csv(
            Constant.PATH_FOLDER_PROCESSED + self._class_file_prefix.replace('/', '_') + '.csv',
            index_col = False
        )
        self._class_desc_csv = pd.read_csv(
            Constant.PATH_FOLDER_PROCESSED + self._class_desc_file_prefix.replace('/', '_') + '.csv',
            index_col = False
        )

    def _clean(self):
        # add program column    
        self._class_csv = self._class_csv.merge(self._class_desc_csv, on = 'id', how = 'left')
        # filter time (TO DO: Transfer data filterings from ForecastingV2.py to here)
        time_overlap_condition = self._class_csv.apply(lambda row: self._helper.is_time_interval_overlap(row['start_time'], row['end_time'], self._start_time, self._end_time), axis=1)
        self._class_csv = self._class_csv[time_overlap_condition]
        # program_id should be an integer
        self._class_csv = self._class_csv.dropna()
        self._class_csv['program_id'] = self._class_csv['program_id'].astype(int)
        # create demand column
        self._class_csv['demand'] = self._class_csv['capacity'] + self._class_csv['waitlist']
        self._class_csv.drop(columns=['capacity', 'waitlist'], inplace = True)
        # create group column
        self._class_csv['location_id_str'] = self._class_csv['location_id'].astype(str) 
        self._class_csv['program_id_str'] = self._class_csv['program_id'].astype(str) 
        self._class_csv['group'] = self._class_csv['program_id_str'] + '-' + self._class_csv['location_id_str']
        self._class_csv.drop(columns=['location_id_str'], inplace = True)
        self._class_csv.drop(columns=['program_id_str'], inplace = True)
        # group by the 'date' and 'group' column and calculate the average of 'demand'
        self._class_csv = self._class_csv.groupby(['date', 'group']).agg({
            'studio_id': 'first',  # agregate by taking the first value
            'location_id': 'first',  # agregate by taking the first value
            'program_id': 'first',  # agregate by taking the first value
            'day': 'first',  # agregate by taking the first value
            'demand': 'mean'  # agregate by taking the mean
        }).reset_index()
        self._class_csv.drop(columns=['group'], inplace = True)
        # save processed data
        self._class_csv.to_csv(Constant.PATH_CSV_DEMAND, index=False, quoting=csv.QUOTE_NONNUMERIC)

    def preprocess(self, force_fetch: bool):
        if force_fetch or self._is_processed() == False:
            # download raw data
            self._clean_raw_files()
            self._download()
            # read data
            self._read()
            # preprocess
            self._clean()
