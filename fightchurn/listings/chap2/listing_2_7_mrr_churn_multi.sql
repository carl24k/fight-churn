WITH
calc_dates AS (
SELECT generate_series('%from_yyyy-mm-dd'::date
                     , '%to_yyyy-mm-dd'::date
                     , interval '1 month') AS start_date
),
start_accounts AS
(
    SELECT DISTINCT d.start_date, account_id, sum(mrr) as total_mrr, avg(bill_period_months) as bill_period
    FROM SUBSCRIPTION s INNER JOIN calc_dates d ON
    s.START_DATE<= d.start_date
    AND (s.END_DATE>d.start_date or s.END_DATE is null)
    group by account_id, d.start_date
),
end_accounts AS
(
    SELECT DISTINCT d.start_date, account_id, sum(mrr) as total_mrr, avg(bill_period_months) as bill_period
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
	and e.bill_period <= s.bill_period
),
extension_accounts as
(
	select s.start_date, s.account_id, s.total_mrr-e.total_mrr as extension_amount
	from start_accounts s
	inner join end_accounts e on s.account_id=e.account_id
	and s.start_date = e.start_date
	where e.total_mrr < s.total_mrr
	and e.bill_period > s.bill_period
),

start_mrr as (
	select start_date, sum (start_accounts.total_mrr) as start_sum
	from start_accounts
	group by start_date
),
churn_mrr as (
	select start_date,	sum(churned_accounts.total_mrr) as churn_sum
	from churned_accounts
	group by start_date
),
downsell_mrr as (
	select start_date, coalesce(sum(downsell_amount),0.0) as downsell_sum
    from downsell_accounts
    group by start_date
),
extension_mrr as (
	select start_date, coalesce(sum(extension_amount),0.0) as extension_sum
    from extension_accounts
    group by start_date
)
SELECT s.start_date,(s.start_date+interval '1 month')::date as end_date,
    start_sum as start_mrr,  coalesce(churn_sum,0) as churn_mrr, coalesce(downsell_sum,0) as downsell_mrr, coalesce(extension_sum,0) as extension_mrr,
	( coalesce(churn_sum,0)+coalesce(downsell_sum,0)) /start_sum as mrr_churn_rate,
    1.0-(1-(( coalesce(churn_sum,0)+coalesce(downsell_sum,0)) /start_sum ))^12 as annual_mrr_churn_rate,
	( coalesce(extension_sum,0)) /start_sum as mrr_extension_rate,
    1.0-(1-(( coalesce(extension_sum,0)) /start_sum ))^12 as annual_mrr_extension_rate
FROM start_mrr s
full outer join churn_mrr c
on s.start_date=c.start_date
full outer join downsell_mrr d
on d.start_date = s.start_date
full outer join extension_mrr x
on x.start_date = s.start_date
order by s.start_date;