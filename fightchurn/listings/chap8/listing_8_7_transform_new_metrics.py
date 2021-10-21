from sklearn.pipeline import Pipeline
from joblib import load
import pandas as pd

def transform_new_metrics(data_set_path, new_data_path):

    scorer_path = data_set_path.replace('.csv', '_extreme_transformer.pkl')
    reducer_path = data_set_path.replace('.csv', '_hc_dimreduce_transform.pkl')

    scorer = load(scorer_path)
    scorer.reset_out_col()
    reducer = load(reducer_path)
    reducer.reset_out_col()

    transfomer_pipeline = Pipeline([('score', scorer), ('reduce', reducer)])

    data_df = pd.read_csv(new_data_path,index_col=[0,1])

    groupscore_data = transfomer_pipeline.transform(data_df)

    score_save_path = data_set_path.replace('.csv', '_groupscore.csv')
    groupscore_data.to_csv(score_save_path, header=True)
    print('Saving transformed results to %s' % score_save_path)
