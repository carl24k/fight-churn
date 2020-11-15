set search_path = '%schema';
with date_vals AS (
  select i::timestamp as metric_date from generate_series('%from_date', '%to_date', '7 day'::interval) i
)

insert into metric (account_id,metric_time,metric_name_id,metric_value)

select account_id, metric_date,%metric_name_id, (%quotwin)::float/(%measwin::float) *  %fun
from event e inner join date_vals d
on e.event_time <= metric_date and e.event_time > metric_date - interval '%measwin week'
where e.event_type_id=%event_id
group by account_id, metric_date
order by account_id, metric_date;




