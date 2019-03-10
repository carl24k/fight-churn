set search_path = '%schema';
with
date_range as (
	select i::timestamp as calc_date from generate_series('%from_date', '%to_date', '7 day'::interval) i
), the_metric as (
	select * from metric
	where metric_name_id=%metric_name_id
)
select calc_date,  min(metric_value) as min_val, avg(metric_value) as avg_val, max(metric_value) as max_val, count(*) as n_calc
from date_range left outer join the_metric on calc_date=metric_time
group by calc_date
order by calc_date
