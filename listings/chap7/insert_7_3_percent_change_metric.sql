
INSERT into metric_name values (NEW_ID,'NEW_NAME')
ON CONFLICT DO NOTHING;

with end_metric as (
	select account_id, metric_time, metric_value as end_value
	from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = 'METRIC_TO_MEASURE'
	and metric_time between 'FRYR-MM-DD' and 'TOYR-MM-DD'
), start_metric as (
	select account_id, metric_time, metric_value as start_value
	from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = 'METRIC_TO_MEASURE'
	and metric_time between ('FRYR-MM-DD'::timestamp -interval 'PERIOD_WEEKS week')
	    and ('TOYR-MM-DD'::timestamp -interval 'PERIOD_WEEKS week')
)

insert into metric (account_id,metric_time,metric_name_id,metric_value)

select s.account_id, s.metric_time + interval 'PERIOD_WEEKS week', NEW_ID,
    coalesce(end_value,0.0)/start_value - 1.0
from start_metric s left outer join end_metric e
	on s.account_id=e.account_id
	and e.metric_time=(s.metric_time + interval 'PERIOD_WEEKS week')
where start_value > 0
ON CONFLICT DO NOTHING;

