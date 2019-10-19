

INSERT into metric_name values (%new_metric_id,'%new_metric_name')
ON CONFLICT DO NOTHING;

with end_metric as (
	select account_id, metric_time, metric_value as end_value
	from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = '%metric2measure'
	and metric_time between '%from_yyyy-mm-dd' and '%to_yyyy-mm-dd'
), start_metric as (
	select account_id, metric_time, metric_value as start_value
	from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = '%metric2measure'
	and metric_time between ('%from_yyyy-mm-dd'::timestamp -interval '%period_weeks week')
	    and ('%to_yyyy-mm-dd'::timestamp -interval '%period_weeks week')
)

insert into metric (account_id,metric_time,metric_name_id,metric_value)

select s.account_id, s.metric_time + interval '%period_weeks week', %new_metric_id,
    coalesce(end_value,0.0)/start_value - 1.0
from start_metric s left outer join end_metric e
	on s.account_id=e.account_id
	and e.metric_time=(s.metric_time + interval '%period_weeks week')
where start_value > 0
ON CONFLICT DO NOTHING;

