from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.models import DAG
from kaapana.operators.DcmConverterOperator import DcmConverterOperator
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator
from kaapana.operators.LocalMinioOperator import LocalMinioOperator
from kaapana.operators.LocalGetRefSeriesOperator import LocalGetRefSeriesOperator
from sortdicom.SortDicomOperator import SortDicomOperator
from kaapana.operators.LocalDcm2JsonOperator import LocalDcm2JsonOperator
from kaapana.operators.DcmSendOperator import DcmSendOperator


log = LoggingMixin().log


args = {
    'ui_visible': True,
    'owner': 'kaapana',
    'start_date': days_ago(0),
    'retries': 0,
    'retry_delay': timedelta(seconds=30)
}

dag = DAG(
    dag_id='sort-dicom',
    default_args=args,
    schedule_interval=None
    )

get_input = LocalGetInputDataOperator(dag=dag)
sorterT1 = SortDicomOperator(dag=dag, input_operator=get_input,series_description="T1",task_id="T1")
sorterFlair = SortDicomOperator(dag=dag, input_operator=get_input,series_description="FLAIR",task_id="Flair")
extract_metadata_T1 = LocalDcm2JsonOperator(dag=dag, input_operator=sorterT1, delete_private_tags=True,task_id="GetT1Metadata")
extract_metadata_Flair = LocalDcm2JsonOperator(dag=dag, input_operator=sorterFlair, delete_private_tags=True,task_id="GetFlairMetadata")
convertT1 = DcmConverterOperator(dag=dag, input_operator=sorterT1, output_format='nii.gz',task_id="T1_to_nii")
convertFlair = DcmConverterOperator(dag=dag, input_operator=sorterFlair, output_format='nii.gz',task_id="flair_to_nii")
putT1_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[convertT1], file_white_tuples=('.nii.gz'),task_id="putT1")
putFlair_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[convertFlair], file_white_tuples=('.nii.gz'),task_id="putFlair")
clean = LocalWorkflowCleanerOperator(dag=dag,clean_workflow_dir=False)

# get_ref_series = LocalGetRefSeriesOperator(
#     dag=dag,
#     input_operator=get_input,
#     search_policy="study_uid",
#     parallel_downloads=5,
#     modality='MR',
#     dicom_tags=[(0x0008,0x103E)]
# )

#get_input >> get_ref_series >> convert >> put_to_minio >> clean
get_input >> sorterT1 >> convertT1 >> putT1_to_minio >> clean
sorterT1 >> extract_metadata_T1
get_input >> sorterFlair >> convertFlair >> putFlair_to_minio >> clean 
sorterFlair >> extract_metadata_Flair



