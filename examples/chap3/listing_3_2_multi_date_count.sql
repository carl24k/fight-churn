with date_vals AS (
  	select i::timestamp as metric_date 
	from generate_series('FRYR-MM-DD', 'TOYR-MM-DD', '7 day'::interval) i 
)
select account_id, metric_date, count(*) as n_login 
from event e inner join date_vals d
on e.event_time < metric_date
and e.event_time >= metric_date - interval '28 day'
where e.event_type_id=18    
group by account_id, metric_date
order by account_id, metric_date;
