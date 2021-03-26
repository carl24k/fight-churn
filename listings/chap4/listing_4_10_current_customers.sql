with metric_date as
(
    select  max(metric_time) as last_metric_time from metric
)
select m.account_id, d.last_metric_time,
sum(case when metric_name_id=0 then metric_value else 0 end) as ReadingOwnedBook,
sum(case when metric_name_id=1 then metric_value else 0 end) as EBookDownloaded,
sum(case when metric_name_id=2 then metric_value else 0 end) as ReadingFreePreview,
sum(case when metric_name_id=3 then metric_value else 0 end) as HighlightCreated,
sum(case when metric_name_id=4 then metric_value else 0 end) as FreeContentCheckout,
sum(case when metric_name_id=5 then metric_value else 0 end) as ReadingOpenChapter,
sum(case when metric_name_id=6 then metric_value else 0 end) as WishlistItemAdded,
sum(case when metric_name_id=7 then metric_value else 0 end) as CrossReferenceTermOpened,
sum(case when metric_name_id=8 then metric_value else 0 end) as total_events,
sum(case when metric_name_id=9 then metric_value else 0 end) as distinct_products,
sum(case when metric_name_id=10 then metric_value else 0 end) as reading_utilities,
sum(case when metric_name_id=11 then metric_value else 0 end) as downloads_per_book,
sum(case when metric_name_id=12 then metric_value else 0 end) as percent_reading,
sum(case when metric_name_id=13 then metric_value else 0 end) as percent_utilities,
sum(case when metric_name_id=14 then metric_value else 0 end) as events_per_book
from metric m inner join metric_date d on m.metric_time = d.last_metric_time
group by m.account_id, d.last_metric_time
order by m.account_id

