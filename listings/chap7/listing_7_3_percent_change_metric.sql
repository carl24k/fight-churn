with start_metric as (
	select account_id, metric_time, metric_value as start_value
	from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = 'METRIC_TO_MEASURE'
	and metric_time between 'FRYR-MM-DD' and 'TOYR-MM-DD'
), end_metric as (
	select account_id, metric_time, metric_value as end_value
	from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = 'METRIC_TO_MEASURE'
	and metric_time between ('FRYR-MM-DD'::timestamp -interval 'PERIOD_WEEKS week')
	    and ('TOYR-MM-DD'::timestamp -interval 'PERIOD_WEEKS week')
)

select e.account_id, s.metric_time, start_value, end_value, start_value/end_value - 1.0 as metric_pcnt_change
from end_metric e inner join start_metric s
	on s.account_id=e.account_id
	and s.metric_time=(e.metric_time + interval 'PERIOD_WEEKS week')
where end_value > 0;
