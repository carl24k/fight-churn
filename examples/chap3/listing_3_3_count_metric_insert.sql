with date_vals AS (
 	select i::timestamp as metric_date 
from generate_series('FRYR-MM-DD', 'TOYR-MM-DD', '7 day'::interval) i
)
-- insert into metric (account_id,metric_time,metric_name_id,metric_value)  -- UNCOMMENT TO ACTUALLY INSERT
select account_id, metric_date,1,  count(*) AS metric_value
from event e inner join date_vals d
on e.event_time < metric_date 
and e.event_time >= metric_date - interval '28 day'
inner join event_type t on t.event_type_id=e.event_type_id
where t.event_type_name='EVENT_NAME'
group by account_id, metric_date;
