with metric_date as
(
    select  max(metric_time) as last_metric_time
    from metric
    where metric_time <= '%to_yyyy-mm-dd'::timestamp
)
select account_id, last_metric_time FLAT_METRIC_SELECT
from metric inner join metric_date
on metric_time = last_metric_time
group by account_id, last_metric_time
order by account_id, last_metric_time
