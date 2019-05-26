with date_vals AS (
  	select i::timestamp as metric_date
from generate_series('FRYR-MM-DD', 'TOYR-MM-DD', '7 day'::interval) i
)
select account_id, metric_date, sum(mrr)
from subscription inner join date_vals
on start_date <= metric_date
and (end_date > metric_date or end_date is null)
group by account_id, metric_date
