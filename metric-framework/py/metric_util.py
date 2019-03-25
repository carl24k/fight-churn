
def metricIdSql(schema,metric_name):
	return "select metric_name_id from %s.metric_name where metric_name='%s'" % (schema, metric_name)

