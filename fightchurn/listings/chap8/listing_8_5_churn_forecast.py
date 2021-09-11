import pandas as pd
import os
import pickle
import matplotlib.pyplot as plt
from fightchurn.listings.chap8.listing_8_4_rescore_metrics import reload_churn_data

def churn_forecast(data_set_path,model_name='logreg_model'):

    pickle_path = data_set_path.replace('.csv', '_{}.pkl'.format(model_name))
    assert os.path.isfile(pickle_path), 'You must run listing 8.2 to save a logistic regression model first'
    with open(pickle_path, 'rb') as fid:
        logreg_model = pickle.load(fid)

    current_score_df = reload_churn_data(data_set_path,'current_groupscore','8.4',is_customer_data=True)

    predictions = logreg_model.predict_proba(current_score_df.to_numpy())

    predict_df = pd.DataFrame(predictions, index=current_score_df.index, columns=['churn_prob', 'retain_prob'])
    forecast_save_path = data_set_path.replace('.csv', '_current_predictions.csv')
    print('Saving results to %s' % forecast_save_path)
    predict_df.to_csv(forecast_save_path, header=True)

    forecast_histogram(data_set_path,predict_df)

def forecast_histogram(data_set_path,predict_df,ext='reg'):
    plt.figure(figsize=[6,4])
    n, bins,_ = plt.hist(predict_df['churn_prob'].values,bins=20)
    plt.xlabel('Churn Probability')
    plt.ylabel('# of Accounts')
    plt.title('Histogram of Active Customer Churn Probability ({})'.format(ext))
    plt.grid()
    plt.savefig(data_set_path.replace('.csv', '_{}_churnhist.png'.format(ext)), format='png')
    plt.close()
    hist_df=pd.DataFrame({'n':n,'bins':bins[1:]})
    hist_df.to_csv(data_set_path.replace('.csv', '_current_churnhist.csv'))
