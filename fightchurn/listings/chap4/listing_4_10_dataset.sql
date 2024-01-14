with observation_params as     
(
    select  interval '%metric_interval' as metric_period,
    '%from_yyyy-mm-dd'::timestamp as obs_start,
    '%to_yyyy-mm-dd'::timestamp as obs_end
)
select m.account_id, o.observation_date, is_churn,
sum(case when metric_name_id=100 then metric_value else 0 end) as search,
sum(case when metric_name_id=101 then metric_value else 0 end) as create_search,
sum(case when metric_name_id=102 then metric_value else 0 end) as edit_search,
sum(case when metric_name_id=103 then metric_value else 0 end) as delete_search,
sum(case when metric_name_id=104 then metric_value else 0 end) as win_opportunity,
sum(case when metric_name_id=105 then metric_value else 0 end) as advance_stage,
sum(case when metric_name_id=106 then metric_value else 0 end) as add_competitor,
sum(case when metric_name_id=107 then metric_value else 0 end) as disqualify_opportunity,
sum(case when metric_name_id=108 then metric_value else 0 end) as lose_opportunity,
sum(case when metric_name_id=109 then metric_value else 0 end) as quote,
sum(case when metric_name_id=110 then metric_value else 0 end) as create_opportunity,
sum(case when metric_name_id=111 then metric_value else 0 end) as add_contact,
sum(case when metric_name_id=112 then metric_value else 0 end) as edit_contact,
sum(case when metric_name_id=113 then metric_value else 0 end) as add_lead,
sum(case when metric_name_id=114 then metric_value else 0 end) as unsub_lead,
sum(case when metric_name_id=115 then metric_value else 0 end) as edit_lead,
sum(case when metric_name_id=116 then metric_value else 0 end) as email_lead,
sum(case when metric_name_id=117 then metric_value else 0 end) as call_lead,
sum(case when metric_name_id=118 then metric_value else 0 end) as create_list,
sum(case when metric_name_id=119 then metric_value else 0 end) as delete_list,
sum(case when metric_name_id=120 then metric_value else 0 end) as email_list,
sum(case when metric_name_id=121 then metric_value else 0 end) as meeting,
sum(case when metric_name_id=122 then metric_value else 0 end) as schedule_meeting,
sum(case when metric_name_id=123 then metric_value else 0 end) as edit_meeting,
sum(case when metric_name_id=124 then metric_value else 0 end) as cancel_meeting,
sum(case when metric_name_id=25 then metric_value else 0 end) as mrr,
sum(case when metric_name_id=31 then metric_value else 0 end) as opp_value_won,
sum(case when metric_name_id=32 then metric_value else 0 end) as opp_value_lost,
sum(case when metric_name_id=47 then metric_value else 0 end) as mrr_per_dollar_closed

from metric m inner join observation_params
on metric_time between obs_start and obs_end    
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp    
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, is_churn    
order by observation_date,m.account_id
