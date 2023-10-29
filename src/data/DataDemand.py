# type: ignore
import pandas as pd
import csv

from ..data.DataClass import DataClass
from ..data.DataClassDescription import DataClassDesc
from ..entities.Helper import Helper

class DataDemand:
    def __init__(self):
        self._class_csv: pd.DataFrame = pd.DataFrame()
        self._class_desc_csv: pd.DataFrame = pd.DataFrame()
        self._helper = Helper()
        # data
        self._class_file_prefix = 'class'
        self._class_desc_file_prefix = 'class_description'
        # data dependencies
        self._data_class = DataClass()
        self._data_class_desc = DataClassDesc()

    
    def _clean_raw_files(self):
        try:
            file_prefixes = [
                self._class_file_prefix,
                self._class_desc_file_prefix
            ]
            for file_prefix in file_prefixes:
                self._helper.delete_file('data/processed/' + file_prefix.replace('/', '_') + '.csv')
        except:
            # ignore
            pass

    def _download(self):
        self._data_class.preprocess(force_fetch=True)
        self._data_class_desc.preprocess(force_fetch=True)

    def _is_processed(self):
        return self._helper.is_file_present('data/processed', 'demand.csv')

    def _read(self):
        self._class_csv = pd.read_csv(
            'data/processed/' + self._class_file_prefix.replace('/', '_') + '.csv',
            index_col = False
        )
        self._class_desc_csv = pd.read_csv(
            'data/processed/' + self._class_desc_file_prefix.replace('/', '_') + '.csv',
            index_col = False
        )

    def _clean(self):
        # rename class description columns
        self._class_desc_csv.rename(
            columns = {
                'id': 'classid',
                'name': 'program',
            },
            inplace = True
        )
        # add program column    
        self._class_csv = self._class_csv.merge(self._class_desc_csv, on = 'classid', how = 'left')
        # create demand column
        self._class_csv['demand'] = self._class_csv['capacity'] + self._class_csv['waitlist']
        self._class_csv.drop(columns=['capacity', 'waitlist'], inplace = True)
        # create group column
        self._class_csv['location_str'] = self._class_csv['location'].astype(str) 
        self._class_csv['program_str'] = self._class_csv['program'].astype(str) 
        self._class_csv['group'] = self._class_csv['program_str'] + '-' + self._class_csv['location_str']
        self._class_csv.drop(columns=['location_str'], inplace = True)
        self._class_csv.drop(columns=['program_str'], inplace = True)
        # group by the 'date' and 'group' column and calculate the average of 'demand'
        self._class_csv = self._class_csv.groupby(['date', 'group']).agg({
            'studio': 'first',  # agregate by taking the first value
            'location': 'first',  # agregate by taking the first value
            'program': 'first',  # agregate by taking the first value
            'day': 'first',  # agregate by taking the first value
            'demand': 'mean'  # agregate by taking the mean
        }).reset_index()
        self._class_csv.drop(columns=['group'], inplace = True)
        # save processed data
        self._class_csv.to_csv('data/processed/demand.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

    def preprocess(self, force_fetch: bool):
        if force_fetch or self._is_processed() == False:
            # download raw data
            self._clean_raw_files()
            self._download()
            # read data
            self._read()
            # preprocess
            self._clean()
