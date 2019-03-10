with observation_params as     
(
    select                 7  as metric_period,    
    '2017-01-01'::timestamp as obs_start,    
    '2017-12-31'::timestamp as obs_end    
)
select m.account_id, o.observation_date, is_churn,    
sum(case when metric_type_id=0 then metric_value else 0 end) as account_tenure,    
sum(case when metric_type_id=1 then metric_value else 0 end) as logins_per_month,
sum(case when metric_type_id=2 then metric_value else 0 end) as num_time_spent,
sum(case when metric_type_id=3 then metric_value else 0 end) as avg_time_spent,
sum(case when metric_type_id=4 then metric_value else 0 end) as met4,
sum(case when metric_type_id=5 then metric_value else 0 end) as met5,
sum(case when metric_type_id=6 then metric_value else 0 end) as met6
from metric m inner join observation_params
on metric_time between obs_start and obs_end    
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp    
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, is_churn    
