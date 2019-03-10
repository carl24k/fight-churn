with observation_params as 
(
	select 14 as allowed_gap,
	       7  as lead_time,
	       7  as minimum_length,
	       '2017-01-01'::date as observe_start,
	       '2017-12-31'::date as observe_end
),
end_dates as 
(
	select distinct account_id, end_date, (end_date + allowed_gap)::date as resignup_end
	from subscription cross join observation_params 
	where end_date is not null
	and (end_date - start_date) > minimum_length 
	and end_date < now()::date - allowed_gap
	and end_date between observe_start and observe_end
), 
resignups as 
(
	select distinct e.account_id, e.end_date
	from end_dates e inner join subscription s
	on e.account_id = s.account_id
	and s.start_date <= e.resignup_end
	and s.end_date > e.end_date
	cross join observation_params 
	where (s.end_date-s.start_date) > minimum_length
) 
-- insert into observation (account_id, observation_date, churn_date)
select e.account_id, 
		(e.end_date - lead_time)::date as observation_date,  
		e.end_date as churn_date
from end_dates e left outer join resignups r
on e.account_id = r.account_id
and e.end_date = r.end_date
cross join observation_params
where r.end_date is null
order by account_id, churn_date
