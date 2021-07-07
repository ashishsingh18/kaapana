from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.models import DAG
from kaapana.operators.DcmConverterOperator import DcmConverterOperator
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator
from kaapana.operators.LocalMinioOperator import LocalMinioOperator
from invertimage.InvertImageOperator import InvertImageOperator
from kaapana.operators.Itk2DcmSegOperator import Itk2DcmSegOperator
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
    dag_id='invertimage',
    default_args=args,
    schedule_interval=None
    )


                                       
get_input = LocalGetInputDataOperator(dag=dag)
convert = DcmConverterOperator(dag=dag, output_format='nii.gz')
invert = InvertImageOperator(dag=dag, input_operator=convert)

#alg_name = "InvertedIntensity"
#nrrd2dcmSeg_invertimage = Itk2DcmSegOperator(dag=dag, 
#    input_operator=get_input,
#    segmentation_operator=invert, 
#    single_label_seg_info="Liver",
#    alg_name=alg_name, 
#    series_description=f'{alg_name}')
                                       
put_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[invert], file_white_tuples=('.nii.gz'))
clean = LocalWorkflowCleanerOperator(dag=dag,clean_workflow_dir=False)

# Send DICOM segmentation objects to pacs
#dcmseg_send = DcmSendOperator(dag=dag, input_operator=nrrd2dcmSeg_invertimage)

get_input >> convert >> invert >> put_to_minio >> clean
#get_input >> convert >> invert >> nrrd2dcmSeg_invertimage >> dcmseg_send >> clean


