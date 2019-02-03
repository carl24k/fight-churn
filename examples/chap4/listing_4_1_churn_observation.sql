with observation_periods as (
	select 14 as allowed_gap,
	       7  as lead_time,
	       7  as minimum_length
),
end_dates as (
	select distinct account_id, end_date, min(start_date) as start_date,
		(end_date + allowed_gap)::date as resignup_end, 
		(end_date - lead_time)::date as observation_date
	from subscription inner join observation_periods on 1=1
	where base_plan = true
	and end_date is not null
	and end_date < now()::date - allowed_gap
	and (end_date - start_date) > minimum_length 
	group by account_id, end_date, allowed_gap, lead_time
) 
, resignups as 
(
	select e.account_id, e.end_date, min(s.start_date) as next_start, max(s.end_date) as last_end
	from end_dates e inner join subscription s
	on e.account_id = s.account_id
	and s.start_date <= e.resignup_end
	and s.end_date > e.end_date
	inner join observation_periods on 1=1
	where (s.end_date-s.start_date) > minimum_length
	group by e.account_id, e.end_date
) 
-- insert into observation (account_id, observation_date, churn_date)
select e.account_id,  observation_date,  e.end_date as churn_date
from end_dates e left outer join resignups r
on e.account_id = r.account_id
and e.end_date = r.end_date
where r.end_date is null
and observation_date between '2017-01-01' and '2017-12-31'
order by account_id, churn_date