with RECURSIVE date_range as (   
	select '%to_yyyy-mm-dd'::date as calc_date
),  earlier_starts AS (
	select account_id, min(start_date) as start_date    
	from subscription inner join date_range  
		on start_date <= calc_date
		and (end_date > calc_date or end_date is null)
	group by account_id

	UNION    
	
	select s.account_id, s.start_date    
	from subscription s inner join earlier_starts e 
		on s.account_id=e.account_id    
		and s.start_date < e.start_date    
		and s.end_date >= (e.start_date-31)    
	
) SELECT account_id, min(start_date) as earliest_start,     
calc_date-min(start_date) as subscriber_tenure_days
FROM earlier_starts cross join date_range    
group by account_id, calc_date    
order by account_id;
