from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from services.report_service import generate_hourly_report


def generate_report():
    report = generate_hourly_report()
    print(f"Reporte generado: {report}")


with DAG(
    dag_id="earthquake_hourly_report",
    start_date=datetime(2026, 9, 20),
    schedule="0 * * * *",
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["earthquakes", "reports"],
) as dag:

    generate_hourly_report_task = PythonOperator(
        task_id="generate_hourly_report",
        python_callable=generate_report,
    )
