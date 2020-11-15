set search_path = '%schema';

with num_metric as (
	select account_id, metric_time, metric_value as num_value
	from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = '%mom_metric'
	and metric_time between '%from_date' and '%to_date'
), den_metric as (
	select account_id, metric_time, metric_value as den_value
	from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = '%mom_metric'
	and metric_time between ('%from_date'::timestamp -interval '%mom_win week')
	    and ('%to_date'::timestamp -interval '%mom_win week')
)

insert into metric (account_id,metric_time,metric_name_id,metric_value)

select d.account_id, n.metric_time, %metric_name_id, num_value/den_value - 1.0 as metric_value
from den_metric d inner join num_metric n
	on n.account_id=d.account_id
	and n.metric_time=(d.metric_time + interval '%mom_win week')
where den_value > 0;
