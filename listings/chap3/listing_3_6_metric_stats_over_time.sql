with 
date_range as (     
	select i::timestamp as calc_date 
from generate_series('%from_yyyy-mm-dd', '%to_yyyy-mm-dd', '7 day'::interval) i
), the_metric as (  
	select * from metric m
	inner join metric_name n on m.metric_name_id = n.metric_name_id
	where n.metric_name = '%metric2measure'
)
select calc_date,  avg(metric_value), count(the_metric.*) as n_calc,
min(metric_value), max(metric_value)    
from date_range left outer join the_metric on calc_date=metric_time     
group by calc_date     
order by calc_date    
