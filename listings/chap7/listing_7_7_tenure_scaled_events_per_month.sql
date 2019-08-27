select m.account_id, metric_time, 
    m.metric_value as tenure_metric,    
    count(*) as count_unscaled,    
    (QUOTE_PERIOD/ least(OBS_PERIOD,m.metric_value))  as scaling,
    (QUOTE_PERIOD/ least(OBS_PERIOD,m.metric_value))  * count(*) as EVENT_TO_QUERY_permonth_QUOTE_PERIODday_avg
from event e inner join metric m    on m.account_id = e.account_id
    and event_time <= metric_time
    and event_time >  metric_time-interval 'OBS_PERIOD days'
inner join event_type t on t.event_type_id=e.event_type_id
inner join metric_name  n on m.metric_name_id = n.metric_name_id
where t.event_type_name='EVENT_TO_QUERY'
    and n.metric_name='account_tenure'
    and metric_value >= MIN_TENURE
group by m.account_id, metric_time, metric_value    
order by m.account_id, metric_time, metric_value
