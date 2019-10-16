insert into metric_name values (%new_metric_id,'%new_metric_name')
ON CONFLICT DO NOTHING;

