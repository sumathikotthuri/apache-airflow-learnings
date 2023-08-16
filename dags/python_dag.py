from datetime import  datetime,timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner' : 'sumathi',
    'retries':5,
    'retry_delay': timedelta(minutes=5)
}

def greet(age,ti):
    name = ti.xcom_pull(task_ids='get_name')
    print(f'Hello World! My name is {name}, and my age is {age}')


def get_name():
    return 'krishna'


with DAG(
    default_args=default_args,
    dag_id='python_dag_v05',
    description='First DAG with python operator',
    start_date=datetime(2023,8,15),
    schedule_interval= '@daily'

) as dag:    
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'age':40}
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name        
    )

    task2 >> task1

