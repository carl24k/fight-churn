import pandas as pd
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt


def churn_forecast(data_set_path='',save=True):

    pickle_path = data_set_path.replace('.csv', '_logreg_model.pkl')
    assert os.path.isfile(pickle_path), 'You must run listing 8.2 to save a logistic regression model first'
    with open(pickle_path, 'rb') as fid:
        logreg_model = pickle.load(fid)

    score_save_path=data_set_path.replace('.csv','_current_groupscore.csv')
    assert os.path.isfile(score_save_path), 'You must run listing 8.3 to save current scores first'
    current_score_df=pd.read_csv(score_save_path,index_col=[0,1])

    predictions = logreg_model.predict_proba(current_score_df.to_numpy())

    if save:
        predict_df = pd.DataFrame(predictions, index=current_score_df.index, columns=['churn_prob', 'retain_prob'])
        forecast_save_path = data_set_path.replace('.csv', '_current_predictions.csv')
        print('Saving results to %s' % forecast_save_path)
        predict_df.to_csv(forecast_save_path, header=True)

        plt.figure(figsize=[6,4])
        n, bins,_ = plt.hist(predictions[:,0],bins=20)
        hist_df=pd.DataFrame({'n':n,'bins':bins[1:]})
        plt.xlim(left=0)
        plt.xlabel('Churn Probability')
        plt.ylabel('# of Accounts')
        plt.title('Histogram of Current Churn Probability')
        # plt.gca().get_yaxis().set_ticklabels([])
        # plt.gca().get_xaxis().set_ticklabels([])
        plt.grid()
        plt.savefig(data_set_path.replace('.csv', '_current_churnhist.svg'), format='svg')
        plt.close()
        hist_df.to_csv(data_set_path.replace('.csv', '_current_churnhist.csv'))

    return predictions
