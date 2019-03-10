select m.account_id, metric_time, 
    m.metric_value as tenure_metric,    
    count(*) as count_unscaled,    
    (28.0/ least(182.0,m.metric_value))  as scaling, 
    (28.0/ least(182.0,m.metric_value))  * count(*) as count_per_month_26wk    
from event e inner join metric m    
    on m.account_id = e.account_id  
    	and event_time <= metric_time    
and event_time >  metric_time-interval '182 days'    
where e.event_type_id=39
    and metric_name_id = 0    
    and metric_value >= 14    
group by m.account_id, metric_time, metric_value    
order by m.account_id, metric_time, metric_value
