with 
date_range as (    
	select  '2019-12-01'::timestamp as start_date,
		'2020-06-01'::timestamp as end_date
), account_count as (    
	select count(distinct account_id) as n_account
	from event e inner join date_range d on
	 e.event_time <= d.end_date
	and e.event_Time >= d.start_date
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
group by e.event_type,n_account,end_date,start_date, event_type_name
order by events_per_account_per_month desc;    
