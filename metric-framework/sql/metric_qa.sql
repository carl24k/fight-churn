set search_path = '%schema';
with
date_range as (
	select i::timestamp as calc_date from generate_series('%from_date', '%to_date', '7 day'::interval) i
), the_metric as (
	select * from metric
	where metric_type_id=%metric_type_id
)
select calc_date,  avg(metric_value) as avg_val, count(distinct metric_id) as n_calc
from date_range left outer join the_metric on calc_date=metric_time
group by calc_date
order by calc_date
