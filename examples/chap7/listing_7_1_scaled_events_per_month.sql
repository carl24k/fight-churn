with date_vals AS (    
     select i::timestamp as metric_date 
     from generate_series('FRYR-MM-DD', 'TOYR-MM-DD', '7 day'::interval) i
)
select account_id, metric_date, 
(28)::float/(84)::float * count(*) as n_login     
from event e inner join date_vals d
on e.event_time <= metric_date 
and e.event_time > metric_date - interval 'OBS_INTERVAL'
inner join event_type t on t.event_type_id=e.event_type_id
where t.event_type_name='EVENT_NAME'
group by account_id, metric_date
order by account_id, metric_date;
