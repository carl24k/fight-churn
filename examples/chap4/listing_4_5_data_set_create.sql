with observation_params as     
(
    select  interval 'MET_INTERVAL' as metric_period,
    'FRYR-MM-DD'::timestamp as obs_start,    
    'TOYR-MM-DD'::timestamp as obs_end    
)
select m.account_id, o.observation_date, is_churn,    
sum(case when metric_name_id=0 then metric_value else 0 end) as met0,
sum(case when metric_name_id=1 then metric_value else 0 end) as met1,
sum(case when metric_name_id=2 then metric_value else 0 end) as met2,
sum(case when metric_name_id=3 then metric_value else 0 end) as met3,
sum(case when metric_name_id=4 then metric_value else 0 end) as met4,
sum(case when metric_name_id=5 then metric_value else 0 end) as met5,
sum(case when metric_name_id=6 then metric_value else 0 end) as met6
from metric m inner join observation_params
on metric_time between obs_start and obs_end    
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp    
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, is_churn    
