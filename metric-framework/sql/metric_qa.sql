set search_path = '%schema';
select metric_time, avg(metric_value) as avg_val, count(*) as n_calc
from metric
where metric_type_id=%metric_type_id
group by metric_time
order by metric_time
