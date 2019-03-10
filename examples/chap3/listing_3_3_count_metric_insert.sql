with date_vals AS (
 	select i::timestamp as metric_date 
from generate_series('2017-01-29', '2017-04-16', '7 day'::interval) i
)
insert into metric (account_id,metric_time,metric_name_id,metric_value)
select account_id, metric_date,1,  count(*)
from event e inner join date_vals d
on e.event_time < metric_date 
and e.event_time >= metric_date - interval '28 day'
where e.event_type_id=18
group by account_id, metric_date;
