with calc_date as (
	select '%to_yyyy-mm-dd'::timestamp  as the_date
) 
select account_id, count(*) as n_%event2measure_permonth
from event e inner join calc_date d on
  e.event_time <= d.the_date
  and e.event_time > d.the_date - interval '28 day'
inner join event_type t on t.event_type_id=e.event_type_id
where t.event_type_name='%event2measure'
group by account_id; 
