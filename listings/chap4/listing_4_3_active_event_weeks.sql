WITH
   periods as (    
	select i::timestamp as period_start, i::timestamp + '7 day'::interval as period_end 
	from generate_series('%from_yyyy-mm-dd', '%to_yyyy-mm-dd', '7 day'::interval) i
)
insert into active_week (account_id, start_date, end_date)
select account_id, 
period_start::date,     
period_end::date
from event inner join periods on event_time>=period_start    
	and event_time < period_end     
group by account_id, period_start, period_end    

