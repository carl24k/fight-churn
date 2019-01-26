

with 
date_range as (
	select  '2017-01-01'::date as start_date, 
		'2017-09-01'::date as end_date
), 
start_accounts as 
(
	select distinct account_id
	from subscription s inner join date_range d on
		s.start_date <= d.start_date
		and (s.end_date > d.start_date or s.end_date is null)
),
start_count as (
	select 	count(start_accounts.*) as n_start from start_accounts
), 
end_accounts as 
(
	select distinct account_id
	from subscription s inner join date_range d on
		s.start_date <= d.end_date
		and (s.end_date > d.end_date or s.end_date is null)
), 
end_count as (
	select 	count(end_accounts.*) as n_end from end_accounts
), 
churned_accounts as 
(
	select distinct s.account_id
	from start_accounts s 
	left outer join end_accounts e on 
		s.account_id=e.account_id
	where e.account_id is null
),
churn_count as (
	select 	count(churned_accounts.*) as n_churn from churned_accounts
)
select 
	n_start, 
	n_churn, 
	n_churn::float/n_start::float as measured_churn_rate,
	end_date-start_date as period,
	1.0-power(1-n_churn::float/n_start::float,365.0/(end_date-start_date)::float) as annual_churn_rate,
	1.0-power(1-n_churn::float/n_start::float,(365.0/12.0)/(end_date-start_date)::float) as monthly_churn_rate

from start_count, end_count, churn_count, date_range
