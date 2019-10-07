select account_id, metric_time,
    string_agg(metric_value::text,' + ') as metric_sum,
    sum(metric_value) as metric_total
from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
and n.metric_name in (%metric_list)
where metric_time between '%from_yyyy-mm-dd' and '%to_yyyy-mm-dd'
group by metric_time, account_id
