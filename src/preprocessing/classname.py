# Imports
import pandas as pd
import numpy as np

# Read data
data = pd.read_csv('data/raw/tblclasses_descriptions_44717.csv', usecols=['CLASSID', 'CLASSNAME'])

# Rename the selected columns
data.rename(
    columns = {
        'CLASSID': 'classid',
        'CLASSNAME': 'classname',
    },
    inplace = True
)

# Standardize classname
## Lower case all
data['classname'] = data['classname'].str.lower()
## Remove all spaces
data['classname'] = data['classname'].str.replace(r'\s', '', case=False, regex=True)
## Remove all symbols
data['classname'] = data['classname'].str.replace(r'[^\w\s]', '', case=False, regex=True)
## Remove 'and' word
data['classname'] = data['classname'].str.replace(r'and', '', case=False, regex=False)
## If classname has substring of 'fullbody', replace as 'fullbody' only
data.loc[data['classname'].str.contains('fullbody', case=False), 'classname'] = 'fullbody'
## If classname has substring of 'express', replace as '30minexpress' only
data.loc[data['classname'].str.contains('express', case=False), 'classname'] = '30minexpress'
## If classname has substring of 'foundation', replace as 'foundations' only
data.loc[data['classname'].str.contains('foundation', case=False), 'classname'] = 'foundations'
## If classname has substring of 'advance', replace as 'advanced' only
data.loc[data['classname'].str.contains('advance', case=False), 'classname'] = 'advanced'
## If classname has substring of 'beginner', replace as 'beginner' only
data.loc[data['classname'].str.contains('beginner', case=False), 'classname'] = 'beginner'
## If classname has substring of 'armsabs', replace as 'armsabs' only
data.loc[data['classname'].str.contains('armsabs', case=False), 'classname'] = 'armsabs'
## If classname has substring of 'bunsabs', replace as 'bunsabs' only
data.loc[data['classname'].str.contains('bunsabs', case=False), 'classname'] = 'bunsabs'
## If classname has substring of 'bunsguns', replace as 'bunsguns' only
data.loc[data['classname'].str.contains('bunsguns', case=False), 'classname'] = 'bunsguns'
## If classname has substring of 'training', replace as 'training' only
data.loc[data['classname'].str.contains('training', case=False), 'classname'] = 'training'
## If classname is not one of the allowed values, change to NaN
data.loc[~data['classname'].isin(['30minexpress', 'advanced', 'armsabs', 'beginner', 'bunsabs', 'bunsguns', 'training', 'foundations', 'fullbody']), 'classname'] = np.nan

# Print
print(data.head())
print('Number of rows:', data.shape[0])
print('Unique class ids:', len(data['classid'].unique()))
print('Unique class names:', len(data['classname'].unique()))

# Save
np.savetxt('data/interim/classname.csv', data, delimiter=',', header='classid,classname', fmt='%s', comments='')