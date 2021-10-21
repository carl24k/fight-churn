from sklearn.pipeline import Pipeline
from joblib import load
import pandas as pd

def transform_forecast(data_set_path, new_data_path):

    scorer_path = data_set_path.replace('.csv', '_extreme_transformer.pkl')
    reducer_path = data_set_path.replace('.csv', '_hc_dimreduce_transform.pkl')
    logreg_path = data_set_path.replace('.csv', '_logreg_model.pkl')

    scorer = load(scorer_path)
    scorer.reset_out_col()
    reducer = load(reducer_path)
    reducer.reset_out_col()
    logreg = load(logreg_path)

    model_pipeline = Pipeline([('score', scorer), ('reduce', reducer), ('logreg', logreg)])


    current_data = pd.read_csv(new_data_path,index_col=[0,1])

    predictions = model_pipeline.predict_proba(current_data)

    predict_df = pd.DataFrame(predictions, index=current_data.index, columns=['churn_prob', 'retain_prob'])
    forecast_save_path = data_set_path.replace('.csv', '_current_predictions.csv')
    print('Saving results to %s' % forecast_save_path)
    predict_df.to_csv(forecast_save_path, header=True)