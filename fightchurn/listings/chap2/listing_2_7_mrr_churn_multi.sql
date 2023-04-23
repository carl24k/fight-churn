WITH
calc_dates AS (
SELECT generate_series('%from_yyyy-mm-dd'::date
                     , '%to_yyyy-mm-dd'::date
                     , interval '1 month') AS start_date
),
start_accounts AS
(
    SELECT DISTINCT d.start_date, account_id, sum(mrr) as total_mrr
    FROM SUBSCRIPTION s INNER JOIN calc_dates d ON
    s.START_DATE<= d.start_date
    AND (s.END_DATE>d.start_date or s.END_DATE is null)
    group by account_id, d.start_date
),
end_accounts AS
(
    SELECT DISTINCT d.start_date, account_id, sum(mrr) as total_mrr
    FROM SUBSCRIPTION s INNER JOIN calc_dates d ON
    s.START_DATE<=  (d.start_date+interval '1 month')
    AND (s.END_DATE>(d.start_date+interval '1 month') or s.end_date is null)
    group by account_id, d.start_date
),
churned_accounts AS
(
    SELECT s.start_date, s.account_id, sum(s.total_mrr) as total_mrr
    FROM start_accounts s
    LEFT OUTER JOIN end_accounts e ON
    s.account_id=e.account_id
    and s.start_date = e.start_date
    WHERE e.account_id is null
    group by s.start_date, s.account_id
),
downsell_accounts as
(
	select s.start_date, s.account_id, s.total_mrr-e.total_mrr as downsell_amount
	from start_accounts s
	inner join end_accounts e on s.account_id=e.account_id
	and s.start_date = e.start_date
	where e.total_mrr < s.total_mrr
),

start_mrr as (
	select start_date, sum (start_accounts.total_mrr) as start_mrr
	from start_accounts
	group by start_date
),
churn_mrr as (
	select start_date,	sum(churned_accounts.total_mrr) as churn_mrr
	from churned_accounts
	group by start_date
),
downsell_mrr as (
	select start_date, coalesce(sum(downsell_accounts.downsell_amount),0.0) as downsell_mrr
    from downsell_accounts
    group by start_date
)
SELECT s.start_date,(s.start_date+interval '1 month')::date as end_date,
	100*(churn_mrr+downsell_mrr) /start_mrr as mrr_churn_rate,
    start_mrr, churn_mrr, downsell_mrr
FROM start_mrr s
inner join churn_mrr c
on s.start_date=c.start_date
inner join downsell_mrr d
on d.start_date = s.start_date
order by s.start_date;