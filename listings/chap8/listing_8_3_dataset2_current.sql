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
select s.account_id, d.last_metric_time as observation_date,
sum(case when metric_name_id=0 then metric_value else 0 end) as like_per_month,
sum(case when metric_name_id=1 then metric_value else 0 end) as newfriend_per_month,
sum(case when metric_name_id=2 then metric_value else 0 end) as post_per_month,
sum(case when metric_name_id=3 then metric_value else 0 end) as adview_per_month,
sum(case when metric_name_id=4 then metric_value else 0 end) as dislike_per_month,
sum(case when metric_name_id=34 then metric_value else 0 end) as unfriend_per_month,
sum(case when metric_name_id=6 then metric_value else 0 end) as message_per_month,
sum(case when metric_name_id=7 then metric_value else 0 end) as reply_per_month,
sum(case when metric_name_id=21 then metric_value else 0 end) as adview_per_post,
sum(case when metric_name_id=22 then metric_value else 0 end) as reply_per_message,
sum(case when metric_name_id=23 then metric_value else 0 end) as like_per_post,
sum(case when metric_name_id=24 then metric_value else 0 end) as post_per_message,
sum(case when metric_name_id=25 then metric_value else 0 end) as unfriend_per_newfriend,
sum(case when metric_name_id=27 then metric_value else 0 end) as dislike_pcnt,
sum(case when metric_name_id=30 then metric_value else 0 end) as newfriend_pcnt_chng,
sum(case when metric_name_id=31 then metric_value else 0 end) as days_since_newfriend
from metric m inner join metric_date d on m.metric_time = d.last_metric_time
inner join account_tenures a on a.account_id = m.account_id
inner join subscription s on m.account_id=s.account_id
where s.start_date <= d.last_metric_time
and (s.end_date >= d.last_metric_time or s.end_date is null)
group by s.account_id, d.last_metric_time
order by s.account_id
