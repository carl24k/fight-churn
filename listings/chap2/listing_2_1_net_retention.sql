with 
date_range as (    
	select  '%from_yyyy-mm-dd'::date as start_date, '%to_yyyy-mm-dd'::date as end_date
), 
start_accounts as    
(
	select  account_id, sum (mrr) as total_mrr    
	from subscription s inner join date_range d on
		s.start_date <= d.start_date    
		and (s.end_date > d.start_date or s.end_date is null)
	group by account_id    
),
end_accounts as    
(
	select account_id, sum(mrr) as total_mrr      
	from subscription s inner join date_range d on
		s.start_date <= d.end_date    
		and (s.end_date > d.end_date or s.end_date is null)
	group by account_id    
), 
retained_accounts as     
(
	select s.account_id, sum(e.total_mrr) as total_mrr     
	from start_accounts s 
	inner join end_accounts e on s.account_id=e.account_id  
	group by s.account_id    
),
start_mrr as (    
	select sum (start_accounts.total_mrr) as start_mrr from start_accounts
), 
retain_mrr as (    
	select sum(retained_accounts.total_mrr) as retain_mrr 
from retained_accounts
)
select 
	retain_mrr /start_mrr as net_mrr_retention_rate,    
	1.0 - retain_mrr /start_mrr as net_mrr_churn_rate,    
	start_mrr,    
	retain_mrr
from start_mrr, retain_mrr
