with 
date_range as (    
	select  '%from_yyyy-mm-dd'::timestamp as start_date,
		'%to_yyyy-mm-dd'::timestamp as end_date
), account_count as (    
	select count(distinct account_id) as n_account
	from subscription s inner join date_range d on
	 s.start_date <= d.end_date
	and (s.end_date >= d.start_date or s.end_date is null)
)
select event_type_name, 
    count(*) as n_event,    
    n_account as n_account,  
    count(*)::float/n_account::float as events_per_account,
extract(days from end_date-start_date)::float/28 as n_months,    
(count(*)::float/n_account::float)/(extract(days from end_date-start_date)::float/28.0)  as events_per_account_per_month
from event e cross join account_count    
inner join event_type t on t.event_type_id=e.event_type_id
inner join date_range ON    
	event_time >= start_date
	and event_time <= end_date
group by e.event_type_id,n_account,end_date,start_date, event_type_name    
order by events_per_account_per_month desc;    
