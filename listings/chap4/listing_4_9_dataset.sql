select m.account_id, m.metric_time, is_churn,
sum(case when metric_name_id=0 then metric_value else 0 end) as ReadingOwnedBook,
sum(case when metric_name_id=1 then metric_value else 0 end) as EBookDownloaded,
sum(case when metric_name_id=2 then metric_value else 0 end) as ReadingFreePreview,
sum(case when metric_name_id=3 then metric_value else 0 end) as HighlightCreated,
sum(case when metric_name_id=4 then metric_value else 0 end) as FreeContentCheckout,
sum(case when metric_name_id=5 then metric_value else 0 end) as ReadingOpenChapter,
sum(case when metric_name_id=6 then metric_value else 0 end) as WishlistItemAdded,
sum(case when metric_name_id=7 then metric_value else 0 end) as CrossReferenceTermOpened,
sum(case when metric_name_id=8 then metric_value else 0 end) as TotalEvents,
sum(case when metric_name_id=9 then metric_value else 0 end) as DistinctProducts
from metric m
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - 7)::timestamp
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, is_churn
order by observation_date,m.account_id
