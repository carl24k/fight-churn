with date_vals AS (
     select i::timestamp as metric_date
     from generate_series('FRYR-MM-DD', 'TOYR-MM-DD', '7 day'::interval) i
)
select account_id, metric_date, count(distinct user_id) as n_distinct_users
from event e inner join date_vals d
on e.event_time <= metric_date
and e.event_time > metric_date - interval 'OBS_PERIOD days'
group by account_id, metric_date
order by metric_date, account_id;
