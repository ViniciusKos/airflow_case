from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator


# define arguments of DAG
default_args = {
        'owner': 'Vinicius',
        'depends_on_past': False,
        'email': ['kos.mota28@hotmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 3,
        'retry_delay': timedelta( minutes=1 )
        }


#define DAG
dag = DAG( 
          dag_id='analysis_dag',
          default_args=default_args,
          start_date=datetime( 2022, 12, 18 ),
          end_date=datetime( 2022, 12, 19 ),
          schedule_interval=timedelta( minutes=60 ) )


#define TASKS
task1 = SqliteOperator(
    task_id='query_sqlite',
    sqlite_conn_id='sqlite_conn_id',
    sql=r"""
    SELECT *
    FROM df_airflow
    """,
    dag=dag
)