# Imports
from typing import List, Type, TypeVar
from collections import namedtuple
import csv

# Types
Studios = namedtuple('Studios', ['id', 'name'])
Programs = namedtuple('Programs', ['id', 'name'])
Coaches = namedtuple('Coaches', ['id', 'name'])
Days = namedtuple('Days', ['id', 'name'])

# Helper functions
def load_data():
    T = TypeVar('T')
    def get_data(set_type: Type[T], set_name: str) -> List[T]:
        ret = []
        if set_name == 'days':
            for day in range(30):
                ret.append(set_type('D' + str(day), day))
        else: 
            with open(f'data/processed/{set_name}.csv', 'r') as csv_file:
                data = csv.DictReader(csv_file)
                for row in data:
                    ret.append(set_type(row['id'], row['name']))
        return ret
    return get_data(Studios, 'studios'), get_data(Programs, 'programs'), get_data(Coaches, 'coaches'), get_data(Days, 'days')