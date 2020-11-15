set search_path = '%schema';

insert into metric (account_id,metric_time,metric_name_id,metric_value)

select m.account_id, metric_time, %metric_name_id,
    (%quotwin/ least(%measwin,m.metric_value))  *  %fun
from event e inner join metric m
    on m.account_id = e.account_id
    	and event_time <= metric_time
and event_time >  metric_time-interval '%measwin week'
inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = 'account_tenure'
where e.event_type_id=%event_id
    and metric_value >= %minten
    and metric_time between '%from_date'::timestamp and '%to_date'::timestamp
group by m.account_id, metric_time, metric_value
order by m.account_id, metric_time, metric_value;
