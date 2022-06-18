
"""Testing basic BigQuery connections and the churn dataset."""

import datetime

from airflow import models
from airflow.providers.google.cloud.operators import bigquery
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator


yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is detected in the Cloud Storage bucket.
    'start_date': yesterday,
    'retries': 1,
}


with models.DAG('churn_data_test',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:

    # Copied from Google Example to test connections
    task_default = bigquery.BigQueryInsertJobOperator(
        task_id='task_default_connection',
        configuration={
            "query": {
                "query": 'SELECT 1',
                "useLegacySql": False
            }
        }
    )
    task_explicit = bigquery.BigQueryInsertJobOperator(
        task_id='task_explicit_connection',
        gcp_conn_id='google_cloud_default',
        configuration={
            "query": {
                "query": 'SELECT 1',
                "useLegacySql": False
            }
        }
    )
    # Copied from Blog Post
    check_public = BigQueryCheckOperator(task_id='check_public_event_data',
                                         sql="""
                            select count(*) > 0
                            from bigquery-public-data.austin_bikeshare.bikeshare_trips
                        """,
                                         use_legacy_sql=False)

    # Checking the churn data
    check_private = BigQueryCheckOperator(task_id='check_churn_event_data',
                                          sql="""
                            select count(*) > 0
                            from churn-XXXXX.socialnet7.event
                        """,
                                          location="us-west1",
                                          use_legacy_sql=False)


task_default >> task_explicit >> check_public >> check_private
