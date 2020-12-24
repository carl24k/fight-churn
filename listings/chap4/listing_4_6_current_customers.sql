with metric_date as
(
    select  max(metric_time) as last_metric_time from metric
)
select m.account_id, d.last_metric_time,
sum(case when metric_name_id=0 then metric_value else 0 end) as ReadingOwnedBook_90d,
sum(case when metric_name_id=1 then metric_value else 0 end) as FirstLivebookAccess_90d,
sum(case when metric_name_id=2 then metric_value else 0 end) as FirstManningAccess_90d,
sum(case when metric_name_id=3 then metric_value else 0 end) as EBookDownloaded_90d,
sum(case when metric_name_id=4 then metric_value else 0 end) as ReadingFreePreview_90d,
sum(case when metric_name_id=5 then metric_value else 0 end) as HighlightCreated_90d,
sum(case when metric_name_id=6 then metric_value else 0 end) as FreeContentCheckout_90d,
sum(case when metric_name_id=7 then metric_value else 0 end) as ReadingOpenChapter_90d,
sum(case when metric_name_id=8 then metric_value else 0 end) as TimeReadingOwnedBook_90d
from metric m inner join metric_date d on m.metric_time = d.last_metric_time
group by m.account_id, d.last_metric_time
order by m.account_id

