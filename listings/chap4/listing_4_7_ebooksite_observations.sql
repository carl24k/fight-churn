with first_use as (
select account_id, product_id, min(event_time) as first_use_time
from event
where event_type in ('ReadingOwnedBook','EBookDownloaded')
group by account_id, product_id
order by account_id, first_use_time
),
pre_0301_accounts as (
	select distinct account_id from first_use
	where first_use_time < cast('2020-03-01' as timestamp)
),
post_0301_accounts as (
	select distinct account_id from first_use
	where first_use_time >= cast('2020-03-01' as timestamp)
)
insert into observation (account_id, observation_date, purchase)
select pre.account_id, cast('2020-03-01' as date) as observation_date,
case when post.account_id is null then false else true end as new_purchase
from pre_0301_accounts pre left outer join post_0301_accounts post
on pre.account_id = post.account_id;
