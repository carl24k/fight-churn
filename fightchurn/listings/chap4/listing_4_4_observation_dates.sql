with RECURSIVE observation_params as    
(    
	select interval '%obs_interval' as obs_interval,
	       interval '%lead_time'  as lead_time,
	       '%from_yyyy-mm-dd'::date as obs_start,
	       '%to_yyyy-mm-dd'::date as obs_end
),observations as (    
	select  account_id,
	    start_date,
	    1 as obs_count,
	    (start_date+obs_interval-lead_time)::date as obs_date,
	    case 
	         when churn_date >= (start_date +   obs_interval-lead_time)::date 
		      and churn_date <  (start_date + 2*obs_interval-lead_time)::date
				then true 
		    else false 
		end as is_churn    
	from active_period inner join observation_params
	on (churn_date > (obs_start+obs_interval-lead_time)::date   
or churn_date is null)

	UNION    

	SELECT  o.account_id,
	    o.start_date,
		 obs_count+1 as obs_count,
	    (o.start_date+(obs_count+1)*obs_interval-lead_time)::date as obs_date,
		case 
	        when churn_date >= (o.start_date + (obs_count+1)*obs_interval-lead_time)::date
		      and churn_date < (o.start_date + (obs_count+2)*obs_interval-lead_time)::date
				then true 
			else false 
		end as is_churn     
	from observations o inner join observation_params
	on   (o.start_date+(obs_count+1)*obs_interval-lead_time)::date <= obs_end
	inner join active_period s on s.account_id=o.account_id    
	and  (o.start_date+(obs_count+1)*obs_interval-lead_time)::date >= s.start_date
	and ((o.start_date+(obs_count+1)*obs_interval-lead_time)::date < s.churn_date or churn_date is null)
) 
insert into observation (account_id, observation_date, is_churn)
select distinct account_id, obs_date, is_churn
from observations
inner join observation_params on obs_date between obs_start and obs_end
