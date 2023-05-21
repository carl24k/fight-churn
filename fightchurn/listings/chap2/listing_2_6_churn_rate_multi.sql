WITH
calc_dates AS (
SELECT generate_series('%from_yyyy-mm-dd'::date
                     , '%to_yyyy-mm-dd'::date
                     , interval '1 month') AS start_date
),
start_accounts AS
(
    SELECT DISTINCT d.start_date, account_id
    FROM SUBSCRIPTION s INNER JOIN calc_dates d ON
    s.START_DATE<= d.start_date
    AND (s.END_DATE>d.start_date or s.END_DATE is null)
),
end_accounts AS
(
    SELECT DISTINCT d.start_date, account_id
    FROM SUBSCRIPTION s INNER JOIN calc_dates d ON
    s.START_DATE<=  (d.start_date+interval '1 month')
    AND (s.END_DATE>(d.start_date+interval '1 month') or s.end_date is null)
),
churned_accounts AS
(
    SELECT s.start_date, s.account_id
    FROM start_accounts s
    LEFT OUTER JOIN end_accounts e ON
    s.account_id=e.account_id
    and s.start_date = e.start_date
    WHERE e.account_id is null
),
start_count AS (
    SELECT start_date, COUNT(*)::FLOAT AS n_start 
    FROM start_accounts 
    group by start_date
),
churn_count AS (
    SELECT start_date, COUNT(*)::FLOAT AS n_churn 
    FROM churned_accounts 
    group by start_date
)
SELECT s.start_date,(s.start_date+interval '1 month')::date as end_date,
 n_start, n_churn, n_churn/n_start AS churn_rate,
1.0-(1-(n_churn/n_start ))^12 as annual_churn_rate
FROM start_count s
inner join churn_count c
on s.start_date=c.start_date
order by s.start_date;