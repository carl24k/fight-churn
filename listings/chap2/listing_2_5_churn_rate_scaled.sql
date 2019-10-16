with 
date_range as ( 
	select  '%from_yyyy-mm-dd'::date as start_date, '%to_yyyy-mm-dd'::date as end_date
), 
start_accounts as  
(
	select distinct account_id        
	from subscription s inner join date_range d on
		s.start_date <= d.start_date   
		and (s.end_date > d.start_date or s.end_date is null)
),
end_accounts as 
(
	select distinct account_id  
	from subscription s inner join date_range d on
		s.start_date <= d.end_date   
		and (s.end_date > d.end_date or s.end_date is null)
), 
churned_accounts as 
(
	Select s.account_id
	from start_accounts s 
	left outer join end_accounts e on 
		s.account_id=e.account_id  
	where e.account_id is null    
),
start_count as (   
	select 	count(start_accounts.*) as n_start from start_accounts
), 
churn_count as ( 
	select 	count(churned_accounts.*) as n_churn from churned_accounts
)
select
	n_start,   	
	n_churn, 	
	n_churn::float/n_start::float as measured_churn,  
	end_date-start_date as period_days, 
1.0-power(1.0-n_churn::float/n_start::float,365.0/(end_date-start_date)::float)  
as annual_churn,
1.0-power(1.0-n_churn::float/n_start::float,(365.0/12.0)/(end_date-start_date)::float) 
as monthly_churn
from start_count, churn_count, date_range
