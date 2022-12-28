INSERT into metric_name values (%new_metric_id,'active_users')
ON CONFLICT DO NOTHING;

with date_vals AS (
     select i::timestamp as metric_date
     from generate_series('%from_yyyy-mm-dd', '%to_yyyy-mm-dd', '7 day'::interval) i
)
insert into metric (account_id,metric_time,metric_name_id,metric_value)

select account_id, metric_date,%new_metric_id, count(distinct user_id)
from event e inner join date_vals d
on e.event_time <= metric_date
and e.event_time > metric_date - interval '%obs_period days'
group by account_id, metric_date
order by metric_date, account_id;
