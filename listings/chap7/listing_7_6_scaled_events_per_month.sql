with date_vals AS (    
     select i::timestamp as metric_date 
     from generate_series('%from_yyyy-mm-dd', '%to_yyyy-mm-dd', '7 day'::interval) i
)
select account_id, metric_date, count(*) as total_count,
((QUOTE_PERIOD)::float/(OBS_PERIOD)::float) * count(*) as EVENT_TO_QUERY_QUOTE_PERIODday_avg_OBS_PERIODday_obs
from event e inner join date_vals d
on e.event_time <= metric_date 
and e.event_time > metric_date - interval 'OBS_PERIOD days'
inner join event_type t on t.event_type_id=e.event_type_id
where t.event_type_name='EVENT_TO_QUERY'
group by account_id, metric_date
order by metric_date, account_id;
