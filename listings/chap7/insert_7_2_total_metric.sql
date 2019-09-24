

INSERT into metric_name values (NEW_ID,'NEW_NAME')
ON CONFLICT DO NOTHING;

insert into metric (account_id,metric_time,metric_name_id,metric_value)
select account_id, metric_time, NEW_ID, sum(metric_value) as metric_total
from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
and n.metric_name in (METRIC_LIST)
where metric_time between 'FRYR-MM-DD' and 'TOYR-MM-DD'
group by metric_time, account_id
ON CONFLICT DO NOTHING;

