select m.account_id, m.metric_time, is_churn,
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
from metric m
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - 7)::timestamp
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, is_churn
order by observation_date,m.account_id
