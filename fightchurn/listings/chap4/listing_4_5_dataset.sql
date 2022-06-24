with observation_params as     
(
    select  interval '%metric_interval' as metric_period,
    '%from_yyyy-mm-dd'::timestamp as obs_start,
    '%to_yyyy-mm-dd'::timestamp as obs_end
)
select m.account_id, o.observation_date, is_churn,
sum(case when metric_name_id=0 then metric_value else 0 end) as ReadingOwnedBook,
sum(case when metric_name_id=3 then metric_value else 0 end) as EBookDownloaded,
sum(case when metric_name_id=4 then metric_value else 0 end) as ReadingFreePreview,
sum(case when metric_name_id=5 then metric_value else 0 end) as HighlightCreated,
sum(case when metric_name_id=6 then metric_value else 0 end) as FreeContentCheckout,
sum(case when metric_name_id=7 then metric_value else 0 end) as ReadingOpenChapter,
sum(case when metric_name_id=8 then metric_value else 0 end) as ProductTocLivebookLinkOpened,
sum(case when metric_name_id=9 then metric_value else 0 end) as LivebookLogin,
sum(case when metric_name_id=10 then metric_value else 0 end) as DashboardLivebookLinkOpened,
sum(case when metric_name_id=11 then metric_value else 0 end) as WishlistItemAdded,
sum(case when metric_name_id=12 then metric_value else 0 end) as CrossReferenceTermOpened,
sum(case when metric_name_id=13 then metric_value else 0 end) as SearchMade,
sum(case when metric_name_id=14 then metric_value else 0 end) as SearchResultOpened,
sum(case when metric_name_id=15 then metric_value else 0 end) as LookInsideLinkOpen,
sum(case when metric_name_id=17 then metric_value else 0 end) as ReadingBook_Recalc,
sum(case when metric_name_id=20 then metric_value else 0 end) as total_event,
sum(case when metric_name_id=21 then metric_value else 0 end) as distinct_product,
sum(case when metric_name_id=22 then metric_value else 0 end) as total_freebies,
sum(case when metric_name_id=23 then metric_value else 0 end) as total_highlights,
sum(case when metric_name_id=25 then metric_value else 0 end) as download_per_book,
sum(case when metric_name_id=26 then metric_value else 0 end) as total_time_reading

from metric m inner join observation_params
on metric_time between obs_start and obs_end    
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp    
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, is_churn    
order by observation_date,m.account_id
