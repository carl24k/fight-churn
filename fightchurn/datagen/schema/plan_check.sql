
with limited as (
	select 'users' as behavior
)
,customer_limit as (
	select account_id, start_date, end_date, quantity
	from subscription inner join limited
	on units = limited.behavior
),
user_counts as
(
	select l.account_id, start_date, end_date, count(distinct e.user_id) as n_user
	from event e
	inner join customer_limit l
		on e.account_id = l.account_id
		and e.event_time between l.start_date and l.end_date
	group by l.account_id,start_date, end_date
)
select quantity, max(n_user)
from customer_limit l inner join user_counts u
on l.account_id = u.account_id
and l.start_date = u.start_date
and l.end_date = u.end_date
group by quantity;

with limited as (
	select 'search' as behavior
)
,customer_limit as (
	select account_id, start_date, end_date,
	sum(case when units=limited.behavior then 1 else 0 end) as has_plan
	from subscription cross join limited
	group by account_id, start_date, end_date
), has_plan as
(
	select l.account_id, start_date, end_date, count(*) as n_limited
	from event e
	inner join event_type t on t.event_type_id = e.event_type_id
	inner join limited  on t.event_type_name = limited.behavior
	inner join customer_limit l
		on e.account_id = l.account_id
		and e.event_time between l.start_date and l.end_date
	where l.has_plan=1
	group by l.account_id,start_date, end_date
), no_plan as
(
	select l.account_id, start_date, end_date, count(*) as n_limited
	from event e
	inner join event_type t on t.event_type_id = e.event_type_id
	inner join limited  on t.event_type_name = limited.behavior
	inner join customer_limit l
		on e.account_id = l.account_id
		and e.event_time between l.start_date and l.end_date
	where l.has_plan=0
	group by l.account_id,start_date, end_date
)
select 'has_plan', max(n_limited) as max_limited from has_plan
union
select 'no_plan', max(n_limited) as max_limited from no_plan;


with customer_metrics as (
select s.account_id, product, start_date, end_date, max(metric_value) as metric_value
from subscription s inner join metric e
on s.account_id = e.account_id
and e.metric_time between s.start_date and s.end_date
inner join metric_name t
on t.metric_name_id = e.metric_name_id
where t.metric_name='active_users'
group by s.account_id, product, start_date, end_date
)
select product, min(metric_value), max(metric_value), avg(metric_value)
from customer_metrics
group by product;

