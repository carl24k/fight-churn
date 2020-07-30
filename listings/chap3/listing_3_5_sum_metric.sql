with date_vals AS (    
	select i::timestamp as metric_date 
	from generate_series('2019-12-01', '2020-06-01', '7 day'::interval) i
)
insert into metric (account_id,metric_time,metric_name_id,metric_value)
select account_id, metric_date::date, 8, sum(cast(trim(trailing 's' from additional_data) as float)) as sum_reading
from event e inner join date_vals d
	on e.event_time < metric_date
	and e.event_time >= metric_date - interval '90 day'
where event_type='ReadingOwnedBook'
group by account_id, metric_date
order by account_id, metric_date;