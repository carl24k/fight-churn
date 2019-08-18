select account_id, metric_time, sum(metric_value) as metric_total
from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
and n.metric_name in (METRIC_LIST)
where metric_time between 'FRYR-MM-DD' and 'TOYR-MM-DD'
group by metric_time, account_id
