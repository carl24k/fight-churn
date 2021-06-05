


INSERT into metric_name values (%new_metric_id,'%new_metric_name')
ON CONFLICT DO NOTHING;

insert into metric (account_id,metric_time,metric_name_id,metric_value)
select account_id, metric_time, %new_metric_id, sum(metric_value) as metric_total
from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
and n.metric_name in (%metric_list)
where metric_time between '%from_yyyy-mm-dd' and '%to_yyyy-mm-dd'
group by metric_time, account_id
ON CONFLICT DO NOTHING;

