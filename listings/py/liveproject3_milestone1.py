import xgboost as xgb
import pandas as pd
import numpy as np

train_data_path = '/Users/carl/Documents/churn/fight-churn-output/livebook/livebook_dataset.csv'
forecast_data_path = '/Users/carl/Documents/churn/fight-churn-output/livebook/livebook_current_customers.csv'
forecast_save_path = '/Users/carl/Documents/churn/fight-churn-output/livebook/livebook_customer_forecasts.csv'


training_data = pd.read_csv(train_data_path, index_col=[0, 1])
forecast_data = pd.read_csv(forecast_data_path,index_col=[0,1])
y = training_data['is_churn'].astype(np.bool)
X = training_data.drop(['is_churn'], axis=1)

xgb_model = xgb.XGBClassifier(objective='binary:logistic')
xgb_model.fit(X.values,y)

predictions = xgb_model.predict_proba(forecast_data.values)

predict_df = pd.DataFrame(predictions, index=forecast_data.index, columns=['retain_prob','churn_prob'])

predict_df.to_csv(forecast_save_path, header=True)

