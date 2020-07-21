with 
date_range as (     
	select  '%from_yyyy-mm-dd'::timestamp as start_date,
		'%to_yyyy-mm-dd'::timestamp as end_date
), account_count as (    
	select count(distinct account_id) as n_account    
	from event e inner join date_range d on
	 e.event_time between start_date and end_date
)
select metric_name, 
	count(distinct m.account_id) as count_with_metric,
	n_account as n_account,    
	(count(distinct m.account_id))::float/n_account::float as pcnt_with_metric    ,
	avg(metric_value) as avg_value,    
	min(metric_value) as min_value,    
	max(metric_value) as max_value,
	min(metric_time)  as earliest_metric,
	max(metric_time) as last_metric
from metric m cross join account_count
inner join date_range on    
	metric_time >= start_date
	and metric_time <= end_date
inner join metric_name  n on m.metric_name_id = n.metric_name_id
group by metric_name,n_account
order by metric_name;
