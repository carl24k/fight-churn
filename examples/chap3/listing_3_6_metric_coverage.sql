with 
date_range as (     
	select  'FRYR-MM-DD'::timestamp as start_date, 
		'TOYR-MM-DD'::timestamp as end_date
), account_count as (    
	select count(distinct account_id) as n_account    
	from subscription s inner join date_range d on
	 s.start_date <= d.start_date    
	and (s.end_date >= d.end_date or s.end_date is null)    
)
select metric_name, 
	count(distinct account_id) as count_with_metric,    
	n_account as n_account,    
	100.0*(count(distinct account_id))::float/n_account::float as pcnt_with_metric    ,
	avg(metric_value) as avg_value,    
	min(metric_value) as min_value,    
	max(metric_value) as max_value    
from metric m cross join account_count
inner join date_range on    
	metric_time >= start_date
	and metric_time <= end_date
inner join metric_name  n on m.metric_name_id = n.metric_name_id
group by metric_name,n_account;
