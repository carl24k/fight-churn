
with date_vals AS (
  select i::date as metric_date
	from generate_series('%from_yyyy-mm-dd', '%to_yyyy-mm-dd', '7 day'::interval) i
),
last_event as (
    select account_id, metric_date, max(event_time)::date as last_date
    from event e inner join date_vals d
    on e.event_time::date <= metric_date
    inner join event_type t on t.event_type_id=e.event_type_id
    where t.event_type_name='%event2measure'
    group by account_id, metric_date
    order by account_id, metric_date
)
select account_id, metric_date, last_date,
metric_date - last_date as days_since_event
from last_event
