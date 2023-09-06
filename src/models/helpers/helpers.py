# Imports
from typing import List, NamedTuple, Type, TypeVar
import csv

# Types
class Studios(NamedTuple):
        id: str
        name: str

class Programs(NamedTuple):
        id: str
        name: str

class Coaches(NamedTuple):
        id: str
        name: str

class Days(NamedTuple):
        id: str
        name: str

# Helper functions
def load_data():
    T = TypeVar('T')
    def get_data(set_type: Type[T], set_name: str) -> List[T]:
        ret: List[T] = []
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