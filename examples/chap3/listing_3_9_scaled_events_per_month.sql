with date_vals AS (    
     select i::timestamp as metric_date 
     from generate_series('2017-12-31', '2017-12-31', '7 day'::interval) i
)
select account_id, metric_date, 
(28)::float/(84)::float * count(*) as n_login     
from event e inner join date_vals d
on e.event_time <= metric_date 
and e.event_time > metric_date - interval '84 day'   
where e.event_type_id=18
group by account_id, metric_date
order by account_id, metric_date;
