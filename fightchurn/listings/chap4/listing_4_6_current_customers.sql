with metric_date as
(
    select  max(metric_time) as last_metric_time from metric
)
select m.account_id, d.last_metric_time,
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
sum(case when metric_name_id=15 then metric_value else 0 end) as ProductLookInsideLivebookLinkOpened
from metric m inner join metric_date d on m.metric_time = d.last_metric_time
group by m.account_id, d.last_metric_time
order by m.account_id;
