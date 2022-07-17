
"""Testing basic BigQuery connections and the churn dataset."""

import datetime

from airflow import models
from airflow.providers.google.cloud.operators import bigquery
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator, \
    BigQueryUpsertTableOperator, BigQueryInsertJobOperator


project_id = 'churn-stream'
dataset_name = 'socialnet7'
location = "us-west1"

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is detected in the Cloud Storage bucket.
    'start_date': yesterday,
    'retries': 1,
}

expected_events = [['adview',10000],
                   ['dislike',4000],
                   ['like',20000],
                   ['message',10000],
                   ['newfriend',1500],
                   ['post',10000],
                   ['reply',2500],
                   ['unfriend',50]]


with models.DAG('churn_metric_pipeline',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:

    # Checking the churn data
    connect_test = BigQueryCheckOperator(task_id='check_churn_event_data',
                                         sql="""
                            select count(*) > 0
                            from churn-stream.socialnet7.event
                        """,
                                         location="us-west1",
                                         use_legacy_sql=False)

    event_count_table = BigQueryUpsertTableOperator(
        task_id="upsert_event_count_table",
        project_id = project_id,
        dataset_id=dataset_name,
        location=location,
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

    delete_old_count_rows = BigQueryInsertJobOperator(
        task_id="delete_event_count",
        configuration={
            "query": {
                "query": f"""
                    DELETE FROM `{project_id}.{dataset_name}.events_per_day`
                    where event_date ='{{{{  ds }}}}'
                """,
                "useLegacySql": False,
            }
        },
        location=location,
    )

    event_count_query_job = BigQueryInsertJobOperator(
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
        location=location,
    )

    event_per_day_checks = [
         BigQueryCheckOperator(
             task_id= f'check_{event[0]}_count',
              sql=f"""
                    select event_count > {event[1]}
                    from {project_id}.{dataset_name}.events_per_day
                    where event_name = '{event[0]}'
                    and event_date  = '{{{{  ds }}}}'
                """,
                                  location=location,
                                  use_legacy_sql=False)
        for event in expected_events
    ]

    join_branch = DummyOperator(
        task_id="join_event_check_branch",
        trigger_rule="none_failed"
    )

    metric_table = BigQueryUpsertTableOperator(
        task_id="upsert_metric_table",
        project_id = project_id,
        dataset_id=dataset_name,
        location=location,
        table_resource={
            "tableReference": {"tableId": "metric"},
            "schema" : {
                "fields" : [
                    {
                        "name" : "account_id",
                        "type" : "integer"
                    },
                    {
                        "name" : "metric_date",
                        "type" : "date"
                    },
                    {
                        "name" : "metric_name",
                        "type" : "string"
                    },
                    {
                        "name" : "metric_value",
                        "type" : "float"
                    }
                ]
            }
        },
    )

    delete_old_metric_rows = BigQueryInsertJobOperator(
        task_id="delete_metric",
        configuration={
            "query": {
                "query": f"""
                    DELETE FROM `{project_id}.{dataset_name}.metric`
                    where metric_date ='{{{{  ds }}}}'
                """,
                "useLegacySql": False,
            }
        },
        location=location,
    )
    metric_calcs = [
        BigQueryInsertJobOperator(
            task_id=f"insert_{event[0]}_metric",
            configuration={
                "query": {
                    "query": f"""
                        INSERT INTO `{project_id}.{dataset_name}.metric`
                        SELECT account_id, DATE('{{{{  ds }}}}') as metric_date,  '{event[0]}_per_month' as metric_name, count(*) as metric_value
                        FROM `{project_id}.{dataset_name}.event` e 
                        INNER JOIN `{project_id}.{dataset_name}.event_type` t
                        ON e.event_type_id = t.event_type_id
                        WHERE event_type_name = '{event[0]}'
                        AND event_time <= '{{{{  ds }}}}'
                        AND event_time > date_add('{{{{  ds }}}}',interval -4 WEEK)
                        GROUP BY account_id;
                    """,
                    "useLegacySql": False,
                }
            },
            location=location,
        )

        for event in expected_events
    ]


    metric_join = DummyOperator(
        task_id="join_metric_calc_branch",
        trigger_rule="none_failed"
    )


connect_test \
    >> event_count_table >> delete_old_count_rows \
    >> event_count_query_job >> event_per_day_checks >> join_branch \
    >> metric_table >> delete_old_metric_rows  >> metric_calcs >> metric_join


