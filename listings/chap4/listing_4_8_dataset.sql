with observation_params as     
(
    select  interval '%metric_interval' as metric_period,
    '%from_yyyy-mm-dd'::timestamp as obs_start,
    '%to_yyyy-mm-dd'::timestamp as obs_end
)
select m.account_id, o.observation_date, purchase,
sum(case when metric_name_id=14 then metric_value else 0 end) as ReadingOwnedBook_90d,
sum(case when metric_name_id=15 then metric_value else 0 end) as EBookDownloaded_90d,
sum(case when metric_name_id=22 then metric_value else 0 end) as TotalEvents_90d,
sum(case when metric_name_id=28 then metric_value else 0 end) as NumberBooksRead_90d,
sum(case when metric_name_id=23 then metric_value else 0 end) as DaysSinceLastEvent,
sum(case when metric_name_id=24 then metric_value else 0 end) as Percent_Reading_Own_Book,
sum(case when metric_name_id=27 then metric_value else 0 end) as Total_Reading_Features_90d,
sum(case when metric_name_id=29 then metric_value else 0 end) as Downloads_Per_Book
from metric m inner join observation_params
on metric_time between obs_start and obs_end    
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp    
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, purchase
order by observation_date,m.account_id

