select m.account_id, m.metric_time, is_churn,
sum(case when metric_name_id=0 then metric_value else 0 end) as ReadingOwnedBook_90d,
sum(case when metric_name_id=1 then metric_value else 0 end) as EBookDownloaded_90d,
sum(case when metric_name_id=2 then metric_value else 0 end) as ReadingFreePreview_90d,
sum(case when metric_name_id=3 then metric_value else 0 end) as HighlightCreated_90d,
sum(case when metric_name_id=4 then metric_value else 0 end) as FreeContentCheckout_90d,
sum(case when metric_name_id=5 then metric_value else 0 end) as ReadingOpenChapter_90d,
sum(case when metric_name_id=6 then metric_value else 0 end) as WishlistItemAdded_90d,
sum(case when metric_name_id=7 then metric_value else 0 end) as CrossReferenceTermOpened_90d
from metric m
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - 7)::timestamp
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, is_churn
order by observation_date,m.account_id
