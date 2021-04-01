import os
import pickle
import shap
import matplotlib.pyplot as plt
from listing_8_4_rescore_metrics import reload_churn_data

def shap_explain_xgb(data_set_path):

    pickle_path = data_set_path.replace('.csv', '_xgb_model.pkl')
    assert os.path.isfile(pickle_path), 'You must run listing 9.6 to save an XGB regression model first'
    with open(pickle_path, 'rb') as fid:
        xgb_model = pickle.load(fid)

    current_df = reload_churn_data(data_set_path,'current','8.3',is_customer_data=True)
    explainer = shap.Explainer(xgb_model)
    shap_values = explainer(current_df)
    shap.summary_plot(shap_values, current_df, show=False)
    save_file = data_set_path.replace('.csv', '_shap_summary_xgb.png')
    print(f'Saving SHAP Explanation to {save_file}')
    plt.tight_layout()
    plt.savefig(save_file, format='png')
    plt.close()
