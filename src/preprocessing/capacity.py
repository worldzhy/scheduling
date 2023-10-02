# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read data
data = pd.read_csv('data/raw/tblclasses.csv', usecols=['CLASSDATESTART', 'LOCATIONID', 'CLASSID', 'STUDIOID', 'CLASSTRAINERID', 'CLASSCAPACITY', 'WAITLISTSIZE', 'DAYSUNDAY', 'DAYMONDAY', 'DAYTUESDAY', 'DAYWEDNESDAY', 'DAYTHURSDAY', 'DAYFRIDAY', 'DAYSATURDAY'])

# Rename the selected columns
data.rename(
    columns = {
        'CLASSDATESTART': 'date',
        'LOCATIONID': 'location',
        'CLASSID': 'classid',
        'STUDIOID': 'studio',
        'CLASSTRAINERID': 'coach',
        'DAYSUNDAY': 'sunday',
        'DAYMONDAY': 'monday',
        'DAYTUESDAY': 'tuesday',
        'DAYWEDNESDAY': 'wednesday',
        'DAYTHURSDAY': 'thursday',
        'DAYFRIDAY': 'friday',
        'DAYSATURDAY': 'saturday',
        'CLASSCAPACITY': 'capacity',
        'WAITLISTSIZE': 'waitlist',
    },
    inplace = True
)

# Date as date
data['date'] = pd.to_datetime(data['date'], errors='coerce').dt.date

# Aggregate days in single column
data['day'] = None
days_of_week = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
for day in days_of_week:
    data.loc[data[day], 'day'] = day
data.drop(columns=days_of_week, inplace=True)

# Add class names
classname_tbl = pd.read_csv('data/interim/classname.csv')
data = data.merge(classname_tbl, on='classid', how='left')
data.rename(
    columns = {
        'classname': 'program',
    },
    inplace = True
)

# Create demand column
data['demand'] = data['capacity'] + data['waitlist']
data.drop(columns=['capacity', 'waitlist'], inplace=True)

# Move capacity to be the rightmost columns
data = data[['studio', 'date', 'location', 'program', 'coach',  'day', 'demand']]

# Use only location == 4 and program == fullbody for now
data = data[data['location'] == 4]
data = data[data['program'] == 'fullbody']

# Drop coach for now (not part of the independent variable)
data.drop(columns=['coach'], inplace=True)

# Group by the 'date' column and calculate the average of 'value'
data = data.groupby('date').agg({
    'studio': 'first',  # Take the first value (mode for categorical)
    'location': 'first',  # Take the first value (mode for categorical)
    'program': 'first',  # Take the first value (mode for categorical)
    'day': 'first',  # Take the first value (mode for categorical)
    'demand': 'mean'  # Calculate the mean for numerical
}).reset_index()

# Explore data
print('Number of rows:', data.shape[0])
print('Unique date:', len(data['date'].unique()))
print(data.head())

# Save
np.savetxt('data/interim/capacity-location4-programfullbody.csv', data, delimiter=',', header='date,studio,location,program,day,demand', fmt='%s', comments='')