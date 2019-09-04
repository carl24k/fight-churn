

INSERT into metric_name values (NEW_ID,'EVENT_TO_QUERY_QUOTE_PERIODday_avg_OBS_PERIODday_obs_scaled')
ON CONFLICT DO NOTHING;


insert into metric (account_id,metric_time,metric_name_id,metric_value)

select m.account_id, metric_time, NEW_ID,
    (QUOTE_PERIOD/ least(OBS_PERIOD,m.metric_value))  * count(*)
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
ON CONFLICT DO NOTHING;
