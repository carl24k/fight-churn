set search_path = '%schema';
with date_vals AS (
  select i::timestamp as metric_date from generate_series('%from_date', '%to_date', '7 day'::interval) i
),
last_event as (
    select account_id, metric_date, max(event_time) as max_time
    from event e inner join date_vals d
    on e.event_time <= metric_date
    where e.event_type_id=%event_id
    group by account_id, metric_date
    order by account_id, metric_date
)
insert into metric (account_id,metric_time,metric_name_id,metric_value)
select account_id, metric_date, %metric_name_id, extract(days from metric_date - max_time)::integer as metric_value
from last_event
