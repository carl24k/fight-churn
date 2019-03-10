with 
date_range as (     
	select i::timestamp as calc_date 
from generate_series('2017-01-08', '2017-12-31', '7 day'::interval) i
), the_metric as (  
	select * from metric
	where metric_name_id=4
)
select calc_date,  avg(metric_value), count(distinct metric_id) as n_calc,
min(metric_value), max(metric_value)    
from date_range left outer join the_metric on calc_date=metric_time     
group by calc_date     
order by calc_date    
