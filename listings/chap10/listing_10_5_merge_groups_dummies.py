import pandas as pd


def merge_groups_dummies(data_set_path):

    dummies_path = data_set_path.replace('.csv', '_dummies_groupscore.csv')
    dummies_df =pd.read_csv(dummies_path,index_col=[0,1])
    dummies_df.drop(['is_churn'],axis=1,inplace=True)

    groups_path = data_set_path.replace('.csv', '_nocat_groupscore.csv')
    groups_df = pd.read_csv(groups_path,index_col=[0,1])

    merged_df= groups_df.merge(dummies_df,left_index=True,right_index=True)
    save_path = data_set_path.replace('.csv', '_groupscore.csv')
    merged_df.to_csv(save_path)
    print('Saved merged group score + dummy dataset ' + save_path)

    cols = list(merged_df.columns.values)
    cols.remove('is_churn')
    merged_col_df = pd.DataFrame(cols,index=cols,columns=['metrics'])
    merged_col_df.to_csv(data_set_path.replace('.csv', '_groupmets.csv'))
