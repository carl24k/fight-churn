set search_path = '%schema';
with date_vals AS (
  select i::timestamp as metric_date from generate_series('%from_date', '%to_date', '7 day'::interval) i
)

insert into metric (account_id,metric_name_id,metric_time,metric_value)

select account_id, %metric_name_id, metric_date, sum(coalesce(quantity,%fill))
from subscription inner join date_vals
on start_date <= metric_date and (end_date >= metric_date or end_date is null)
where product = '%name'
group by account_id, metric_date

