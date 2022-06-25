
"""Testing basic BigQuery connections and the churn dataset."""

import datetime

from airflow import models
from airflow.providers.google.cloud.operators import bigquery
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator, BigQueryUpsertTableOperator, BigQueryInsertJobOperator

project_id = 'churn-test-353716'
dataset_name = 'socialnet7'

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is detected in the Cloud Storage bucket.
    'start_date': yesterday,
    'retries': 1,
}


with models.DAG('event_count_table_per_day',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:

    # Checking the churn data & Connection
    check_private = BigQueryCheckOperator(task_id='check_churn_event_data',
                                          sql=f"""
                            select count(*) > 0
                            from {project_id}.{dataset_name}.event
                        """,
                                          location="us-west1",
                                          use_legacy_sql=False)

    event_count_table = BigQueryUpsertTableOperator(
        task_id="upsert_table",
        project_id = project_id,
        dataset_id=dataset_name,
        location="us-west1",
        table_resource={
            "tableReference": {"tableId": "events_per_day"},
            "schema" : {
                "fields" : [
                    {
                        "name" : "event_name",
                        "type" : "string"
                    },
                    {
                        "name" : "event_date",
                        "type" : "date"
                    },
                    {
                        "name" : "event_count",
                        "type" : "integer"
                    }
                ]
            }
        },
    )

    insert_query_job = BigQueryInsertJobOperator(
        task_id="insert_event_count",
        configuration={
            "query": {
                "query": f"""
                    INSERT INTO `{project_id}.{dataset_name}.events_per_day`
                    select event_type_name as event_name, date(event_time) as event_date, count(*) as event_count
                    from `{project_id}.{dataset_name}.event` e 
                    inner join `{project_id}.{dataset_name}.event_type` t
                    on e.event_type_id = t.event_type_id
                    where date(event_time)='{{{{  ds }}}}'
                    group by event_type_name, event_date
                    order by event_date, event_name;
                """,
                "useLegacySql": False,
            }
        },
        location='us-west1',
    )


check_private >> event_count_table >> insert_query_job
