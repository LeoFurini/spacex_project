import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.utils.config import load_apis_config, GCS_BUCKET
from src.pipeline.extract_task import extract_and_save_raw
from src.pipeline.transform_task import transform_raw_to_processed
from src.pipeline.load_task import load_processed_to_bq

default_args = {
    "owner": "data-engineer",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(dag_id="config_driven_api_to_bq",
         start_date=datetime(2025, 1, 1),
         schedule_interval="@daily",
         catchup=False,
         default_args=default_args,
         max_active_runs=1) as dag:

    apis = load_apis_config()

    for api_conf in apis:
        api_name = api_conf["name"]

        with TaskGroup(group_id=f"{api_name}_group") as tg:
            extract = PythonOperator(
                task_id=f"{api_name}_extract",
                python_callable=lambda conf=api_conf: extract_and_save_raw(conf)
            )

            transform = PythonOperator(
                task_id=f"{api_name}_transform",
                python_callable=lambda ti, conf=api_conf: transform_raw_to_processed(conf, ti.xcom_pull(task_ids=f"{api_name}_extract"))
            )

            load = PythonOperator(
                task_id=f"{api_name}_load",
                python_callable=lambda ti, conf=api_conf: load_processed_to_bq(conf, ti.xcom_pull(task_ids=f"{api_name}_transform"))
            )

            # wire them: extract >> transform >> load
            extract >> transform >> load

        # if desired, you can set ordering between APIs here

