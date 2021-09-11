with RECURSIVE active_period_params as    
(
    select interval '%gap_interval'  as allowed_gap,
    '%to_yyyy-mm-dd'::date as calc_date
),
active as  
(
	select distinct account_id, min(start_date) as start_date    
	from subscription inner join active_period_params 
on start_date <= calc_date    
		and (end_date > calc_date or end_date is null)
	group by account_id

	UNION

	select s.account_id, s.start_date  
	from subscription s 
	cross join active_period_params 
	inner join active e on s.account_id=e.account_id  
		and s.start_date < e.start_date  
		and s.end_date >= (e.start_date-allowed_gap)::date  

) 
insert into active_period (account_id, start_date, churn_date)     
select account_id, min(start_date) as start_date, NULL::date as churn_date  
from active
group by account_id, churn_date  
