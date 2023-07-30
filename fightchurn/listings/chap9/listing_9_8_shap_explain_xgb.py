import os
import pandas as pd
import pickle
import shap
import matplotlib.pyplot as plt
from fightchurn.listings.chap8.listing_8_2_logistic_regression import prepare_data
from fightchurn.listings.chap8.listing_8_4_rescore_metrics import reload_churn_data

def shap_explain_xgb(data_set_path, plot_n=None, save_values=False):

    pickle_path = data_set_path.replace('.csv', '_xgb_model.pkl')
    assert os.path.isfile(pickle_path), 'You must run listing 9.6 to save an XGB regression model first'
    with open(pickle_path, 'rb') as fid:
        xgb_model = pickle.load(fid)

    # current_df = reload_churn_data(data_set_path,'current','8.3',is_customer_data=True)
    X, y = prepare_data(data_set_path, ext='', as_retention=False)
    explainer = shap.TreeExplainer(xgb_model,feature_perturbation = "interventional", model_output='probability',data=X)
    shap_values = explainer(X)
    shap.summary_plot(shap_values, X, show=False)
    save_file = data_set_path.replace('.csv', '_shap_summary_xgb.png')
    print(f'Saving SHAP Explanation to {save_file}')
    plt.tight_layout()
    plt.savefig(save_file, format='png')
    plt.close()

    if save_values:
        shap_data = pd.DataFrame(shap_values.values,columns=X.columns)
        save_path = data_set_path.replace('.csv', '_shapvals.csv')
        shap_data.to_csv(save_path,header=True)
        print('Saved shap values data to ' + save_path)
        shap_summary = pd.DataFrame(shap_data.describe()).transpose()
        save_path = data_set_path.replace('.csv', '_shapsummary.csv')
        shap_summary.to_csv(save_path,header=True)

    if plot_n is not None:
        for n in plot_n:
            shap.waterfall_plot(shap_values[n],show=False)
            save_file = data_set_path.replace('.csv', f'_shap_water_xgb_{n}.png')
            plt.tight_layout()
            plt.savefig(save_file, format='png')
            plt.close()
