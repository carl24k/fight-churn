with date_vals AS (    
     select i::timestamp as metric_date 
     from generate_series('%from_yyyy-mm-dd', '%to_yyyy-mm-dd', '7 day'::interval) i
)
select account_id, metric_date, count(*) as total_count,
((%desc_period)::float/(%obs_period)::float) * count(*) as %event2measure_%desc_periodday_avg_%obs_periodday_obs
from event e inner join date_vals d
on e.event_time <= metric_date 
and e.event_time > metric_date - interval '%obs_period days'
inner join event_type t on t.event_type_id=e.event_type_id
where t.event_type_name='%event2measure'
group by account_id, metric_date
order by metric_date, account_id;
