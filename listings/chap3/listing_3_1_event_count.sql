with calc_date as (
	select '%to_yyyy-mm-dd'::timestamp  as the_date
) 
select account_id, count(*) as n_%event2measure_permonth
from event e inner join calc_date d on
  e.event_time <= d.the_date
  and e.event_time > d.the_date - interval '28 day'
where event_type='%event2measure'
group by account_id; 
