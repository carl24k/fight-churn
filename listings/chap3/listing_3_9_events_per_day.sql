with
date_range as (    
	select i::timestamp as calc_date 
from generate_series('%from_yyyy-mm-dd', '%to_yyyy-mm-dd', '1 day'::interval) i
)
select event_time::date as event_date,   
	count(*) as n_event
  	/* , sum(%field2sum) as total_%event2measure_%field2sum */
from date_range left outer join event e on calc_date=event_time::date
where event_type ='%event2measure'
group by event_date    
order by event_date
