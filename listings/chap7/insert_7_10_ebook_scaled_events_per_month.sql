insert into metric (account_id,metric_time,metric_name_id,metric_value)

select m.account_id, metric_time,
    %new_metric_id,
    (%desc_period/ least(%obs_period,m.metric_value))  * count(*)
    as metric_value
from event e inner join metric m    on m.account_id = e.account_id
    and event_time <= metric_time
    and event_time >  metric_time-interval '%obs_period days'
inner join metric_name  n on m.metric_name_id = n.metric_name_id
where event_type ='%event2measure'
    and n.metric_name='account_tenure'
    and metric_value >= %min_tenure
group by m.account_id, metric_time, metric_value    
order by m.account_id, metric_time, metric_value
ON CONFLICT DO NOTHING;
