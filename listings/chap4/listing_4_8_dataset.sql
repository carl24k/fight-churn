with observation_params as     
(
    select  interval '%metric_interval' as metric_period,
    '%from_yyyy-mm-dd'::timestamp as obs_start,
    '%to_yyyy-mm-dd'::timestamp as obs_end
)
select m.account_id, o.observation_date, purchase,
sum(case when metric_name_id=14 then metric_value else 0 end) as ReadingOwnedBook_90d,
sum(case when metric_name_id=15 then metric_value else 0 end) as EBookDownloaded_90d,
sum(case when metric_name_id=16 then metric_value else 0 end) as ReadingFreePreview_90d,
sum(case when metric_name_id=17 then metric_value else 0 end) as HighlightCreated_90d,
sum(case when metric_name_id=18 then metric_value else 0 end) as FreeContentCheckout_90d,
sum(case when metric_name_id=19 then metric_value else 0 end) as ReadingOpenChapter_90d,
sum(case when metric_name_id=20 then metric_value else 0 end) as WishlistItemAdded_90d,
sum(case when metric_name_id=21 then metric_value else 0 end) as CrossReferenceTermOpened_90d,
sum(case when metric_name_id=22 then metric_value else 0 end) as TotalEvents_90d,
sum(case when metric_name_id=9 then metric_value else 0 end) as NumberBooksRead_90d
/* sum(case when metric_name_id=10 then metric_value else 0 end) as reads_per_book_90d,
sum(case when metric_name_id=11 then metric_value else 0 end) as downloads_per_book_90d,
sum(case when metric_name_id=12 then metric_value else 0 end) as events_per_book_90d */
from metric m inner join observation_params
on metric_time between obs_start and obs_end    
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp    
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, purchase
order by observation_date,m.account_id

