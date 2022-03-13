with date_vals AS (
 	select i::timestamp as metric_date 
from generate_series('2020-02-22', '2020-06-01', '28 day'::interval) i
)
insert into metric (account_id,metric_time,metric_name_id,metric_value)
select account_id, metric_date, %new_metric_id,  count(distinct product_id) AS metric_value
from event e inner join date_vals d
on e.event_time < metric_date 
and e.event_time >= metric_date - interval '84 day'
group by account_id, metric_date
ON CONFLICT DO NOTHING;
