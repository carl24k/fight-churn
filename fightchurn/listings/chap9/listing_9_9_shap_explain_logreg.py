import os
import pickle
import shap
import matplotlib.pyplot as plt
from fightchurn.listings.chap8.listing_8_4_rescore_metrics import reload_churn_data

def shap_explain_logreg(data_set_path):

    pickle_path = data_set_path.replace('.csv', '_logreg_model_churn.pkl')
    assert os.path.isfile(pickle_path), 'You must run listing 8.2 with param as_retention=False to save a churn logistic regression model first'
    with open(pickle_path, 'rb') as fid:
        logreg_model = pickle.load(fid)

    current_df = reload_churn_data(data_set_path,'current_groupscore','8.4',is_customer_data=True)
    explainer_mask = shap.maskers.Impute(data=current_df)
    explainer = shap.LinearExplainer(logreg_model, masker=explainer_mask, model_output='probability')
    shap_values = explainer(current_df)
    shap.summary_plot(shap_values, current_df, show=False)
    save_file = data_set_path.replace('.csv', '_shap_summary_logreg.png')
    print(f'Saving SHAP Explanation to {save_file}')
    plt.tight_layout()
    plt.savefig(save_file, format='png')
    plt.close()
