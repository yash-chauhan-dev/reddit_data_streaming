from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.reddit_pipeline import reddit_pipeline

default_args = {"owner": "Yash Chauhan", "start_date": datetime(2024, 1, 8)}

file_postfix = datetime.now().strftime("%Y%m%d")

dag = DAG(
    dag_id="etl_reddit_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["reddit", "etl", "pipeline"],
)

# Extraction from reddit

extract = PythonOperator(
    task_id="reddit_extraction",
    python_callable=reddit_pipeline,
    op_kwargs={
        "file_name": f"reddit_{file_postfix}",
        "subreddit": "dataengineering",
        "time_filter": "day",
        "limit": 100,
    },
    dag=dag,
)
