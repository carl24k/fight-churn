with calc_date as (
	select 'TOYR-MM-DD'::timestamp  as the_date   
) 
select account_id, count(*) as n_login
from event e inner join calc_date d on
  e.event_time <= d.the_date
  and e.event_time > d.the_date - interval '28 day'
where e.event_type_id=1
group by account_id; 
