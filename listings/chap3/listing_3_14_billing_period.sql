with date_vals AS (
  	select i::timestamp as metric_date
from generate_series('%from_yyyy-mm-dd', '%to_yyyy-mm-dd', '7 day'::interval) i
)
select account_id, metric_date, min(bill_period_months) as billing_period
from subscription inner join date_vals
on start_date <= metric_date
and (end_date > metric_date or end_date is null)
group by account_id, metric_date
