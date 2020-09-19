with RECURSIVE date_vals AS (    
select i::timestamp as metric_date     
from generate_series('%from_yyyy-mm-dd', '%to_yyyy-mm-dd', '7 day'::interval) i
),
start_date AS (
	select account_id, min(event_time) as first_use_time
    from event
    group by account_id
    order by account_id
)

insert into metric (account_id,metric_time,metric_name_id, metric_value)

SELECT account_id, metric_date, %new_metric_id as metric_name_id,
 extract(days from metric_date - first_use_time) as metric_value
from start_date inner join date_vals
on metric_date >= first_use_time

ON CONFLICT DO NOTHING;
