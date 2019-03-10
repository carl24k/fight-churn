with
date_range as (    
	select i::timestamp as calc_date 
from generate_series('FRYR-MM-DD', 'TOYR-MM-DD', '1 day'::interval) i
)
select event_time::date as event_date,   
	count(*) as n_event,    
  	sum(event_property) as property_sum    
from date_range left outer join event on calc_date=event_time::date  
where event_type_id=%event_type_id    
group by event_date    
order by event_date
