# Imports
import pandas as pd
import numpy as np

# Read data
data = pd.read_csv('data/raw/tblclasses_descriptions_44717.csv', usecols=['CLASSID', 'CLASSNAME'])

# Rename the selected columns
data.rename(
    columns = {
        'CLASSID': 'class_id',
        'CLASSNAME': 'class_name',
    },
    inplace = True
)

# Standardize class_name
## Lower case all
data['class_name'] = data['class_name'].str.lower()
## Remove all spaces
data['class_name'] = data['class_name'].str.replace(r'\s', '', case=False, regex=True)
## Remove all symbols
data['class_name'] = data['class_name'].str.replace(r'[^\w\s]', '', case=False, regex=True)
## Remove 'and' word
data['class_name'] = data['class_name'].str.replace(r'and', '', case=False, regex=False)
## If classname has substring of 'fullbody', replace as 'fullbody' only
data.loc[data['class_name'].str.contains('fullbody', case=False), 'class_name'] = 'fullbody'
## If classname has substring of 'express', replace as '30minexpress' only
data.loc[data['class_name'].str.contains('express', case=False), 'class_name'] = '30minexpress'
## If classname has substring of 'foundation', replace as 'foundations' only
data.loc[data['class_name'].str.contains('foundation', case=False), 'class_name'] = 'foundations'
## If classname has substring of 'advance', replace as 'advanced' only
data.loc[data['class_name'].str.contains('advance', case=False), 'class_name'] = 'advanced'
## If classname has substring of 'beginner', replace as 'beginner' only
data.loc[data['class_name'].str.contains('beginner', case=False), 'class_name'] = 'beginner'
## If classname has substring of 'armsabs', replace as 'armsabs' only
data.loc[data['class_name'].str.contains('armsabs', case=False), 'class_name'] = 'armsabs'
## If classname has substring of 'bunsabs', replace as 'bunsabs' only
data.loc[data['class_name'].str.contains('bunsabs', case=False), 'class_name'] = 'bunsabs'
## If classname has substring of 'bunsguns', replace as 'bunsguns' only
data.loc[data['class_name'].str.contains('bunsguns', case=False), 'class_name'] = 'bunsguns'
## If classname has substring of 'training', replace as 'training' only
data.loc[data['class_name'].str.contains('training', case=False), 'class_name'] = 'training'
## If classname is not one of the allowed values, change to NaN
data.loc[~data['class_name'].isin(['30minexpress', 'advanced', 'armsabs', 'beginner', 'bunsabs', 'bunsguns', 'training', 'foundations', 'fullbody']), 'class_name'] = np.nan

# Print
print(data.head())
print('Number of rows:', data.shape[0])
print('Unique class ids:', len(data['class_id'].unique()))
print('Unique class names:', len(data['class_name'].unique()))

# Save
np.savetxt('data/interim/classname.csv', data, fmt='%s')