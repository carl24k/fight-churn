with RECURSIVE active_period_params as    
(
	select INTERVAL '%gap_interval' as allowed_gap,
	       '%to_yyyy-mm-dd'::date as observe_end,
	       '%from_yyyy-mm-dd'::date as observe_start
),
end_dates as    
(
	select distinct account_id, start_date, end_date, 
(end_date +  allowed_gap)::date as extension_max
	from subscription inner join active_period_params 
	on end_date between observe_start and observe_end    
), 
resignups as     
(
	select distinct e.account_id, e.end_date   
	from end_dates e inner join subscription s on e.account_id = s.account_id
		and s.start_date <= e.extension_max
		and (s.end_date > e.end_date or s.end_date is null)      
),
churns as    
(
	select e.account_id, e.start_date, e.end_date as churn_date    
	from end_dates e left outer join resignups r  
	on e.account_id = r.account_id    
		and e.end_date = r.end_date
	where r.end_date is null    

	UNION

	select s.account_id, s.start_date, e.churn_date    
	from subscription s 
	cross join active_period_params
	inner join churns e on s.account_id=e.account_id
		and s.start_date < e.start_date
		and s.end_date >= (e.start_date- allowed_gap)::date
) 
insert into active_period (account_id, start_date, churn_date)    
select account_id, min(start_date) as start_date, churn_date  
from churns
group by account_id, churn_date
