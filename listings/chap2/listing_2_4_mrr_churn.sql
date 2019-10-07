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
churned_accounts as    
(
	select s.account_id, sum(s.total_mrr) as total_mrr    
	from start_accounts s 
	left outer join end_accounts e on     
		s.account_id=e.account_id
	where e.account_id is null    
	group by s.account_id    	
),
downsell_accounts as    
(
	select s.account_id, s.total_mrr-e.total_mrr as downsell_amount    
	from start_accounts s 
	inner join end_accounts e on s.account_id=e.account_id    
	where e.total_mrr < s.total_mrr    
),
start_mrr as (    
	select sum (start_accounts.total_mrr) as start_mrr from start_accounts
), 
churn_mrr as (    
	select 	sum(churned_accounts.total_mrr) as churn_mrr from churned_accounts
), 
downsell_mrr as (    
	select coalesce(sum(downsell_accounts.downsell_amount),0.0) as downsell_mrr
from downsell_accounts
)
select 
	(churn_mrr+downsell_mrr) /start_mrr as mrr_churn_rate,    
	start_mrr,    
	churn_mrr, 
	downsell_mrr
from start_mrr, churn_mrr, downsell_mrr
