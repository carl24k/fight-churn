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
retained_accounts as
(
	select  s.start_date, s.account_id, sum(e.total_mrr) as total_mrr
	from start_accounts s
	inner join end_accounts e on s.account_id=e.account_id
	and s.start_date = e.start_date
	group by s.account_id, s.start_date
),
start_mrr as (
	select start_date, sum (start_accounts.total_mrr) as start_mrr
	from start_accounts
	group by start_date
),
retained_mrr as (
	select start_date,	sum(retained_accounts.total_mrr) as retained_mrr
	from retained_accounts
	group by start_date
)
SELECT s.start_date,(s.start_date+interval '1 month')::date as end_date,
	retained_mrr /start_mrr as net_retention_rate,
    start_mrr, retained_mrr,
    (retained_mrr /start_mrr )^12 as annual_net_retention_rate
FROM start_mrr s
inner join retained_mrr r
on s.start_date=r.start_date
order by s.start_date;