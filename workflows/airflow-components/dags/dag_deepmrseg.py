from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.models import DAG
from kaapana.operators.DcmConverterOperator import DcmConverterOperator
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator
from kaapana.operators.LocalMinioOperator import LocalMinioOperator
from deepmrseg.DeepMRSegOperator import DeepMRSegOperator
from kaapana.operators.Itk2DcmSegOperator import Itk2DcmSegOperator
from kaapana.operators.DcmSendOperator import DcmSendOperator


log = LoggingMixin().log


args = {
    'ui_visible': True,
    'owner': 'kaapana',
    'start_date': days_ago(0),
    'retries': 0,
    'retry_delay': timedelta(seconds=60)
}

dag = DAG(
    dag_id='deepmrseg',
    default_args=args,
    schedule_interval=None
    )


                                       
get_input = LocalGetInputDataOperator(dag=dag)
convert = DcmConverterOperator(dag=dag, input_operator=get_input, output_format='nii.gz')
dmrs = DeepMRSegOperator(dag=dag, input_operator=convert)

#put_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[dmrs], file_white_tuples=('.nrrd'))
clean = LocalWorkflowCleanerOperator(dag=dag,clean_workflow_dir=False)

#the below pipeline works and sends nrrd to minio
#get_input >> convert >> dmrs >> put_to_minio >> clean

#-----------
#convert nrrd to dicom seg object and send to pacs
alg_name = "SkullStripping"
nrrd2dcmSeg_brain = Itk2DcmSegOperator(dag=dag, 
    segmentation_operator=dmrs, 
    single_label_seg_info="Brain",
    alg_name=alg_name, 
    series_description=f'{alg_name} - Brain')

dcmseg_send_brain = DcmSendOperator(dag=dag, input_operator=nrrd2dcmSeg_brain)

get_input >> convert >> dmrs >> nrrd2dcmSeg_brain >> dcmseg_send_brain >> clean