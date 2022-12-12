set search_path='%schema';
WITH calc_dates AS (
SELECT generate_series(date(min(start_date))
                     , max(start_date)-interval '1month'
                     , interval '1 month') AS start_date
FROM   subscription
),
start_accounts AS
(
    SELECT DISTINCT d.start_date, account_id, mrr
    FROM SUBSCRIPTION s INNER JOIN calc_dates d ON
    s.START_DATE<= d.start_date
    AND (s.END_DATE>d.start_date or s.END_DATE is null)
),
end_accounts AS
(
    SELECT DISTINCT d.start_date, account_id, mrr
    FROM SUBSCRIPTION s INNER JOIN calc_dates d ON
    s.START_DATE<=  (d.start_date+interval '1 month')
    AND (s.END_DATE>(d.start_date+interval '1 month') or s.end_date is null)
),
churned_accounts AS
(
    SELECT s.start_date, s.account_id, s.mrr
    FROM start_accounts s
    LEFT OUTER JOIN end_accounts e ON
    s.account_id=e.account_id
    and s.start_date = e.start_date
    WHERE e.account_id is null
),
start_count AS (
    SELECT start_date, COUNT(*)::FLOAT AS n_start , mrr
    FROM start_accounts
    group by start_date, mrr
),
churn_count AS (
    SELECT start_date, COUNT(*)::FLOAT AS n_churn , mrr
    FROM churned_accounts
    group by start_date, mrr
)
SELECT s.mrr,n_start,n_churn, date(s.start_date),(s.start_date+interval '1 month')::date as end_date,
round(cast((n_churn* 1.0/n_start )*100 as numeric), 2)
AS churn_rate
FROM start_count s
inner join churn_count c
on s.start_date=c.start_date
and s.mrr=c.mrr
order by s.start_date, s.mrr;
