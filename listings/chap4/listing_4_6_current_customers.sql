with metric_date as
(
    select  max(metric_time) as last_metric_time from metric
),
account_tenures as (
    select account_id, metric_value as account_tenure
    from metric m inner join metric_date on metric_time =last_metric_time
    where metric_name_id = 8
    and metric_value >= 14
)
select m.account_id, d.last_metric_time,
sum(case when metric_name_id=0 then metric_value else 0 end) as like_per_month,
sum(case when metric_name_id=1 then metric_value else 0 end) as newfriend_per_month,
sum(case when metric_name_id=2 then metric_value else 0 end) as post_per_month,
sum(case when metric_name_id=3 then metric_value else 0 end) as adview_feed_per_month,
sum(case when metric_name_id=4 then metric_value else 0 end) as dislike_per_month,
sum(case when metric_name_id=5 then metric_value else 0 end) as unfriend_per_month,
sum(case when metric_name_id=6 then metric_value else 0 end) as message_per_month,
sum(case when metric_name_id=7 then metric_value else 0 end) as reply_per_month,
sum(case when metric_name_id=8 then metric_value else 0 end) as account_tenure
from metric m inner join metric_date d on m.metric_time = d.last_metric_time
inner join subscription s on m.account_id=s.account_id
inner join account_tenures a on a.account_id = m.account_id
where s.start_date <= d.last_metric_time
and (s.end_date >= d.last_metric_time or s.end_date is null)
group by m.account_id, d.last_metric_time
order by m.account_id
