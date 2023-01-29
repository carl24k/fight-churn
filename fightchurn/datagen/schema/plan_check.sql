
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


with customer_events as (
select s.account_id, product, start_date, end_date, count(distinct user_id) as n_user
from subscription s inner join event e
on s.account_id = e.account_id
and e.event_time between s.start_date and s.end_date
inner join event_type t
on t.event_type_id = e.event_type_id
where t.event_type_name='schedule_meeting'
group by s.account_id, product, start_date, end_date
)
select product, min(n_user), max(n_user), avg(n_user)
from customer_events
group by product;