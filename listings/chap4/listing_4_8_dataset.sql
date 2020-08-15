with observation_params as     
(
    select  interval '%metric_interval' as metric_period,
    '%from_yyyy-mm-dd'::timestamp as obs_start,
    '%to_yyyy-mm-dd'::timestamp as obs_end
)
select m.account_id, o.observation_date, purchase,
sum(case when metric_name_id=0 then metric_value else 0 end) as ReadingOwnedBook_90d,
sum(case when metric_name_id=1 then metric_value else 0 end) as EBookDownloaded_90d,
sum(case when metric_name_id=2 then metric_value else 0 end) as ReadingFreePreview_90d,
sum(case when metric_name_id=3 then metric_value else 0 end) as HighlightCreated_90d,
sum(case when metric_name_id=4 then metric_value else 0 end) as FreeContentCheckout_90d,
sum(case when metric_name_id=5 then metric_value else 0 end) as ReadingOpenChapter_90d,
sum(case when metric_name_id=6 then metric_value else 0 end) as WishlistItemAdded_90d,
sum(case when metric_name_id=8 then metric_value else 0 end) as CrossReferenceTermOpened_90d,
sum(case when metric_name_id=9 then metric_value else 0 end) as SearchMade_90d
from metric m inner join observation_params
on metric_time between obs_start and obs_end    
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp    
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, purchase
order by observation_date,m.account_id

