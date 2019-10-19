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

select s.account_id, s.metric_time + interval '%period_weeks week',
    start_value, end_value,
    coalesce(end_value,0.0)/start_value - 1.0 as percent_change
from start_metric s left outer join end_metric e
	on s.account_id=e.account_id
	and e.metric_time=(s.metric_time + interval '%period_weeks week')
where start_value > 0

