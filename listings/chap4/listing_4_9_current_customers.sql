with metric_date as
(
    select  max(metric_time) as last_metric_time from metric
)
select m.account_id, d.last_metric_time,
sum(case when metric_name_id=14 then metric_value else 0 end) as ReadingOwnedBook_90d,
sum(case when metric_name_id=15 then metric_value else 0 end) as EBookDownloaded_90d,
sum(case when metric_name_id=22 then metric_value else 0 end) as TotalEvents_90d,
sum(case when metric_name_id=28 then metric_value else 0 end) as NumberBooksRead_90d,
sum(case when metric_name_id=23 then metric_value else 0 end) as DaysSinceLastEvent,
sum(case when metric_name_id=24 then metric_value else 0 end) as Percent_Reading_Own_Book,
sum(case when metric_name_id=29 then metric_value else 0 end) as Downloads_Per_Book,
sum(case when metric_name_id=31 then metric_value else 0 end) as Reading_Feature_Ratio

from metric m inner join metric_date d on m.metric_time = d.last_metric_time
group by m.account_id, d.last_metric_time
order by m.account_id
