with 
date_range as (    
	select  '%from_yyyy-mm-dd'::timestamp as start_date,
		'%to_yyyy-mm-dd'::timestamp as end_date
), account_count as (    
	select count(distinct account_id) as n_account
	from event
)
select event_type,
    count(*) as n_event,
    n_account as n_account,
    count(*)::float/n_account::float as events_per_account,
extract(days from end_date-start_date)::float/28 as n_months,
(count(*)::float/n_account::float)/(extract(days from end_date-start_date)::float/28.0)  as events_per_account_per_month
from event e cross join account_count
inner join date_range ON
	event_time >= start_date
	and event_time <= end_date
group by e.event_type,n_account,end_date,start_date
order by events_per_account_per_month desc;    
