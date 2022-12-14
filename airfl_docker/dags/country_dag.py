import os
import json
import pandas as pd

from airflow                  import DAG
from datetime                 import datetime, timedelta
from airflow.operators.bash   import BashOperator
from airflow.operators.python import PythonOperator

def clean_data():
    filename = str( datetime.now().date() ) + '.json'
    tot_name = os.path.join( os.path.dirname(__file__),'src/data', filename )
    
    with open( tot_name, 'r' ) as inputfile:
        doc = json.load( inputfile )

    # extract data
    df_raw = {
        'id'        : doc['data']['id'],
        'name'      : doc['data']['name'],
    }

    # convert data to csv
    df = pd.DataFrame( df_raw, index=[0] )

    end_path=os.path.join( os.path.dirname(__file__), 'src/data', 'country.csv' )
    df.to_csv( end_path )


# Airflow DAG
default_args = {
        'owner': 'Vinicius',
        'depends_on_past': False,
        'email': ['kos.mota28@hotmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 3,
        'retry_delay': timedelta( minutes=1 )
        }

# define the DAG
dag = DAG( 
          dag_id='country_dag',
          default_args=default_args,
          start_date=datetime( 2022, 12, 11 ),
          schedule_interval=timedelta( minutes=60 ) )

# first task - Get data from API
task1 = BashOperator(
    task_id='get_country',
    bash_command=r'python /opt/airflow/dags/country_dag.py',
    dag = dag )


# second task - Data transformation
task2 = PythonOperator(
        task_id='clean_data',
        provide_context=True,
        python_callable=clean_data,
        dag=dag )




# tasks dependency
task1 >> task2
