set search_path = '%schema';

insert into metric (account_id,metric_time,metric_name_id,metric_value)

select account_id, metric_time, %metric_name_id , sum(metric_value)
from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
and n.metric_name in (%metric_names)
where metric_time between '%from_date'::timestamp and '%to_date'::timestamp
group by account_id, metric_time
