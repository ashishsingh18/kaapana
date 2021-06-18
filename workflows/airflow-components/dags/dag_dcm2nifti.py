from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.models import DAG
from kaapana.operators.DcmConverterOperator import DcmConverterOperator
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator
from kaapana.operators.LocalMinioOperator import LocalMinioOperator


log = LoggingMixin().log


args = {
    'ui_visible': True,
    'owner': 'kaapana',
    'start_date': days_ago(0),
    'retries': 0,
    'retry_delay': timedelta(seconds=30)
}

dag = DAG(
    dag_id='dcm2nifti',
    default_args=args,
    schedule_interval=None
    )


get_input = LocalGetInputDataOperator(dag=dag)
convert = DcmConverterOperator(dag=dag, output_format='nii.gz')
put_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[convert], file_white_tuples=('.nii.gz'))
clean = LocalWorkflowCleanerOperator(dag=dag,clean_workflow_dir=False)

get_input >> convert >> put_to_minio >> clean


