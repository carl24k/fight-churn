select m.account_id, metric_time,
    m.metric_value as tenure_metric,    
    count(*) as count_unscaled,    
    (%desc_period/ least(%obs_period,m.metric_value))  as scaling,
    (%desc_period/ least(%obs_period,m.metric_value))  * count(*)
    as total_events_scaled
from event e inner join metric m    on m.account_id = e.account_id
    and event_time <= metric_time
    and event_time >  metric_time-interval '%obs_period days'
inner join metric_name  n on m.metric_name_id = n.metric_name_id
where  n.metric_name='account_tenure'
    and metric_value >= %min_tenure
group by m.account_id, metric_time, metric_value    
order by m.account_id, metric_time, metric_value
