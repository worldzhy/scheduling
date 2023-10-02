# type: ignore
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Constants
DAYS_OF_WEEK = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

# Read data
data = pd.read_csv(
    'data/raw/tblclasses.csv',
    usecols = ['CLASSDATESTART', 'LOCATIONID', 'CLASSID', 'STUDIOID', 'CLASSTRAINERID', 'CLASSCAPACITY', 'WAITLISTSIZE', 'DAYSUNDAY', 'DAYMONDAY', 'DAYTUESDAY', 'DAYWEDNESDAY', 'DAYTHURSDAY', 'DAYFRIDAY', 'DAYSATURDAY'],
    index_col=False
)

# Rename the selected columns
data.rename(
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

# Convert the date column to datetime
data['date'] = pd.to_datetime(data['date'], errors = 'coerce').dt.date

# Aggregate days in single column called day
data['day'] = None
for day in DAYS_OF_WEEK:
    data.loc[data[day], 'day'] = day
data.drop(columns = DAYS_OF_WEEK, inplace = True)

# Add program column
data = data.merge(pd.read_csv('data/interim/classname.csv'), on = 'classid', how = 'left')
data.rename(
    columns = { 'classname': 'program' },
    inplace = True
)

# Create demand column
data['demand'] = data['capacity'] + data['waitlist']
data.drop(columns=['capacity', 'waitlist'], inplace = True)

# Drop coach for now (not part of the independent variable)
data.drop(columns = ['coach'], inplace = True)

# Remove rows with NA
data = data.dropna()

# Rearrange columns
data = data[['date', 'studio', 'location', 'day', 'program', 'demand']]

# Get unique locations and unique programs
locations = data['location'].unique()
programs = data['program'].unique()

# Create dataframe for processed data
data_processed = pd.DataFrame()

# Aggregate rows by date and group by program-location pair
for loc in locations:
    for prog in programs:
        # Filter data by location and program
        data_temp = data[data['location'] == loc]
        data_temp = data[data['program'] == prog]

        # Group by the 'date' column and calculate the average of 'demand'
        data_temp = data_temp.groupby('date').agg({
            'studio': 'first',  # Agregate by taking the first value
            'location': 'first',  # Agregate by taking the first value
            'program': 'first',  # Agregate by taking the first value
            'day': 'first',  # Agregate by taking the first value
            'demand': 'mean'  # Agregate by taking the mean
        }).reset_index()

        # Create new column called group
        data_temp['group'] = f'{prog}-{loc}'

        # Sort rows by date
        data_temp = data_temp.sort_values(by = 'date')

        # Concatenate current data group to main processed data
        data_processed = pd.concat([data_processed, data_temp], ignore_index = True)

# Save processed data
np.savetxt(
    'data/processed/capacity.csv',
    data_processed,
    delimiter = ',',
    header = 'date, studio, location, day, program, demand, group',
    fmt = '%s',
    comments = ''
)
