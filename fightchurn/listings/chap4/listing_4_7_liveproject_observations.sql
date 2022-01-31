with first_reads as (
	select distinct account_id,product_id,min(event_time) as min_time
	from event
	where event_type in  ('ReadingOwnedBook','EBookDownloaded')
	group by account_id, product_id
), before_march as (
	select distinct account_id
	from first_reads
	where min_time between '2019-12-01' and '2020-02-29'
), after_march as (
	select distinct account_id
	from first_reads
	where min_time between '2020-03-01' and '2020-05-31'
)

insert into observation (account_id, observation_date, is_churn)

select b.account_id, '2020-03-01',
case when a.account_id is null then true else false end as is_churn
from before_march b left outer join after_march a
on b.account_id= a.account_id;
