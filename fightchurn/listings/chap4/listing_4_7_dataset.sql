with observation_params as     
(
    select  interval '%metric_interval' as metric_period,
    '%from_yyyy-mm-dd'::timestamp as obs_start,
    '%to_yyyy-mm-dd'::timestamp as obs_end
)
select m.account_id, o.observation_date, is_churn,
sum(case when metric_name_id=11 then metric_value else 0 end) as advance_stage,
sum(case when metric_name_id=12 then metric_value else 0 end) as close_opportunity,
sum(case when metric_name_id=13 then metric_value else 0 end) as search,
sum(case when metric_name_id=14 then metric_value else 0 end) as add_competition,
sum(case when metric_name_id=15 then metric_value else 0 end) as revert_stage,
sum(case when metric_name_id=16 then metric_value else 0 end) as lose_opportunity,
sum(case when metric_name_id=17 then metric_value else 0 end) as meeting_held,
sum(case when metric_name_id=18 then metric_value else 0 end) as schedule_meeting,
sum(case when metric_name_id=20 then metric_value else 0 end) as mrr,
sum(case when metric_name_id=21 then metric_value else 0 end) as opp_close_per_dollar
from metric m inner join observation_params
on metric_time between obs_start and obs_end    
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp    
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, is_churn    
order by observation_date,m.account_id
