# type: ignore
import pandas as pd
from prophet.plot import plot_plotly, plot_components_plotly
from prophet import Prophet

## import data
data = pd.read_csv('data/interim/capacity-location4-programfullbody.csv')

## preprocess
# date as datetime
data=data[["date","demand"]]
data.columns = ['ds','y']
data['ds'] = pd.to_datetime(data['ds'])

# split train vs test
test = data.iloc[len(data)-50:] # last 50
train = data.iloc[:len(data)-50] # remaining
print(train.head())

# call prophet
m = Prophet()
m.fit(train)
future = m.make_future_dataframe(periods=50) #MS for monthly, H for hourly
forecast = m.predict(future)

forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

m.plot(forecast)