with RECURSIVE observation_params as    
(    
	select interval '1 month' as obs_interval,    
	       interval '1 week'  as lead_time,     
	       '2017-01-01'::date as obs_start,     
	       '2017-12-31'::date as obs_end        
),observations as (    
	select  account_id,     
	    (start_date+obs_interval-lead_time)::date as obs_date,    
	    case 
	         when churn_date >= (start_date +   obs_interval-lead_time)::date 
		    and churn_date < (start_date + 2*obs_interval-lead_time)::date 
				then true 
		    else false 
		end as is_churn    
	from active_period inner join observation_params
	on (churn_date > (obs_start+obs_interval-lead_time)::date   
or churn_date is null)

	UNION    

	SELECT  o.account_id, 
		(obs_date + obs_interval)::date,    
		case 
		when churn_date >= (obs_date+obs_interval)::date 
and churn_date < (obs_date+2*obs_interval)::date 
				then true 
			else false 
		end as is_churn     
	from observations o inner join observation_params
	on (obs_date + obs_interval) <= obs_end    
	inner join active_period s on s.account_id=o.account_id    
	and (obs_date + obs_interval) >= s.start_date    
	and ((obs_date + obs_interval) < s.churn_date or churn_date is null)
) 
insert into observation (account_id, observation_date, is_churn)
select account_id, obs_date, is_churn
from observations
inner join observation_params on obs_date between obs_start and obs_end
