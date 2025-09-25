from datetime import datetime
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from scripts.coleta import rodar_coleta
from scripts.processamento import rodar_processamento

with DAG(
    dag_id='pipeline_clickbus_dataset_final',
    start_date=datetime(2025, 9, 11),
    schedule_interval='@daily',
    catchup=False,
    tags=['clickbus', 'automacao']
) as dag:
    
    task_coleta = PythonOperator(task_id='simular_coleta_de_dados', python_callable=rodar_coleta)
    task_processamento = PythonOperator(task_id='processar_e_gerar_insights', python_callable=rodar_processamento)
    
    task_coleta >> task_processamento