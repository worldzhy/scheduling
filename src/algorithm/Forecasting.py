# type: ignore
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

## import data
data = pd.read_csv('data/processed/forecast.csv')

## preprocess
# date as datetime
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['day_of_week'] = data['date'].dt.dayofweek
data['day'] = data['date'].dt.day
data['month'] = data['date'].dt.month
data['year'] = data['date'].dt.year
# capacity to y, date to ds
# data = data.rename(columns={'capacity': 'y', 'date': 'ds'})
# create unique id
data['unique_id'] = 'A'
# print data
print(data.head())


## data split
X = data[['day_of_week', 'day', 'month', 'year', 'studio', 'program', 'coach']]
y = data['capacity']

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder())  # One-hot encode categorical features
])

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, ['studio', 'program', 'coach'])
    ])

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

pipeline.fit(X, y)

pred = pipeline.predict(X)
plt.scatter(pred, y)




# ## model params
# train = data.loc[data['ds'] < '2022-06-01']
# valid = data.loc[data['ds'] >= '2022-06-01']
# h = 30 

# ## modeling
# models = [
#     make_pipeline(
#         OneHotEncoder(),
#         SimpleImputer(), 
#         RandomForestRegressor(random_state=0, n_estimators=100)
#     )
# ]


# model = MLForecast(models=models,
#                    freq='D',
#                 #    lags=[1,2,4],
#                 #    lag_transforms={
#                 #        1: [(rolling_mean, 4), (rolling_min, 4), (rolling_max, 4)], # aplicado a uma janela W a partir do registro Lag
#                 #    },
#                    date_features=['day', 'month', 'year'],
#                    num_threads=6)

# model.fit(train, id_col='unique_id', time_col='ds', target_col='y')

# # X = data.drop('capacity', axis=1)  # Drop the target column
# # y = data['capacity']  # Select only the target column