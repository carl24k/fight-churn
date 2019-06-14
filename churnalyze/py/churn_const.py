import os



schema_data_dict = {
    'b': 'BroadlyDataSet4',
    'v_orig': 'VersatureDataSet3',
    'v3': 'VersatureDataSet3_0MRRCleaned',
    'v2': 'VersatureDataSet3_0MRRDemo',
    'v': 'VersatureDataSet2',
    'k': 'KlipfolioDataSet4',
    'churnsim2' : 'churnsim2_dataset'
}

max_clips = {
    'num_seats' : 100
}

ax_scale = {
    'v' : 75.0,
    'k' : 110.0,
    'b' : 110.0,
    'churnsim2' : 110.0
}

min_valid = {
    # 'num_seats' : 1,
    # 'mrr' : 1,
    # 'Active_Users_Last_Qtr' : 1,
    # 'base_units' : 1,
    # 'CustomerDetractor_PerMonth' : 0.5
    #, 'num_users' : 1
    'orientation_switch_permonth' : 1
}

group_corr_thresh = {
    'KlipfolioDataSet4' : 0.65,
    'BroadlyDataSet4' : 0.7,
    'churnsim2_dataset' : 0.8
}

skip_metrics = {
    'KlipfolioDataSet4' : ['create_data_source_from_library_permonth','orientation_switch_permonth_12week','download_permonth_4week','download_permonth_26week'],
    'KlipfolioDataSet5' : ['create_data_source_from_library_permonth','orientation_switch_permonth_12week','download_permonth_4week','download_permonth_26week'],
    'BroadlyDataSet4' : ['leadadded_4weekstrailing','viewprivatefeedback_4weekstrailing','viewreviews_4weekstrailing','viewteamscorecard_4weekstrailing','customerdetractor_4weekstrailing','viewstartuperrorpage_4weekstrailing','viewaddfromfile_4weekstrailing','viewswitchlocation_4weekstrailing','viewteamchat_4weekstrailing','callreceived_4weekstrailing','viewsigninpage_4weekstrailing','viewcustomerinfo_4weekstrailing','viewmanageteam_4weekstrailing','viewsettingsmessaging_4weekstrailing','clickedmessagesbutton_4weekstrailing','toggledsendthankyou_4weekstrailing','viewprofile_4weekstrailing']
}


renames = {'Cost_Local_PerMonth'.lower() : "Local Calls Per Month",
           'Cost_LD_Canada_PerMonth'.lower() : 'Domestic Calls Per Month',
           'CustomerAdded_PerMonth'.lower(): "Customers Added Per Month",
           'ReviewUpdated_PerMonth'.lower(): "Reviews Updated Per Month",
           'Account_Active_Today_PerMonth'.lower() : "Days Active Per Month",
           'account_tenure' : "Account Tenure (Days)",
           "mrr" :"Monthly Recurring Revenue",
           'base_units' : 'Number of Devices',
           "CustomerPromoter_PerMonth".lower():"Customer Promoter",
           "CustomerDetractor_PerMonth".lower():"Customer Detractor",
           "Detractor_Rate".lower():"Detractor Rate",
            'Use_Per_Base_Unit'.lower():"Call Per Device",
            'Use_Per_Dollar_MRR'.lower():"Call Per $ MRR",
            'Dollar_MRR_Per_Call_Unit'.lower():"$ MRR Per Call",
            'Dollar_MRR_Per_Base_Unit'.lower():"$ MRR Per Device",
           'Base_Units_per_Dollar_MRR_Per'.lower() : "Devices per Dollar",
           'Active_Users_Last_Qtr'.lower() : 'Active Users',
           'Num_Users'.lower() : 'Licensed Users',
           'User_Utilization'.lower() : 'License Utilization'
           }
