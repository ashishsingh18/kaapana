from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.models import DAG
from kaapana.operators.DcmConverterOperator import DcmConverterOperator
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator
from kaapana.operators.LocalMinioOperator import LocalMinioOperator
from DLICV.DLICVOperator import DLICVOperator

log = LoggingMixin().log


args = {
    'ui_visible': True,
    'owner': 'kaapana',
    'start_date': days_ago(0),
    'retries': 0,
    'retry_delay': timedelta(seconds=30)
}

dag = DAG(
    dag_id='dlicv',
    default_args=args,
    schedule_interval=None
    )


get_input = LocalGetInputDataOperator(dag=dag)
convert = DcmConverterOperator(dag=dag, input_operator=get_input, output_format='nii.gz')
dlicv = DLICVOperator(dag=dag, input_operator=convert, modeldir="/models/DLICV", batch_size=4,task_id="skull_stripping_dlicv")
put_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[dlicv], file_white_tuples=('.nrrd'))
clean = LocalWorkflowCleanerOperator(dag=dag,clean_workflow_dir=False)

get_input >> convert >> dlicv >> put_to_minio >> clean


