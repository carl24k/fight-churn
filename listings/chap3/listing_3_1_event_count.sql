with calc_date as (
	select 'TOYR-MM-DD'::timestamp  as the_date   
) 
select account_id, count(*) as n_EVENT_NAME
from event e inner join calc_date d on
  e.event_time <= d.the_date
  and e.event_time > d.the_date - interval '28 day'
inner join event_type t on t.event_type_id=e.event_type_id
where t.event_type_name='event_to_query'
group by account_id; 
