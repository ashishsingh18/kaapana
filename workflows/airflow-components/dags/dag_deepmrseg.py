from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from airflow.models import DAG
from kaapana.operators.DcmConverterOperator import DcmConverterOperator
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator
from kaapana.operators.LocalMinioOperator import LocalMinioOperator
from deepmrseg.DeepMRSegOperator import DeepMRSegOperator
from kaapana.operators.Itk2DcmSegOperator import Itk2DcmSegOperator
from kaapana.operators.DcmSendOperator import DcmSendOperator
from kaapana.operators.LocalDcm2JsonOperator import LocalDcm2JsonOperator
from deepmrsegreport.DeepMRSegReportOperator import DeepMRSegReportOperator
from kaapana.operators.Pdf2DcmOperator import Pdf2DcmOperator

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

extract_metadata = LocalDcm2JsonOperator(dag=dag, input_operator=get_input, delete_private_tags=True)
#put_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[dmrs], file_white_tuples=('.nrrd'))
clean = LocalWorkflowCleanerOperator(dag=dag,clean_workflow_dir=False)
dmrs_report = DeepMRSegReportOperator(
    dag=dag,
    input_operator=get_input,
    brainmask_operator=dmrs,
    dicom_metadata_json_operator=extract_metadata)

put_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[dmrs_report], file_white_tuples=('.pdf'))
#the below pipeline works and sends nrrd to minio
#get_input >> convert >> dmrs >> put_to_minio >> clean

#-----------
#convert nrrd to dicom seg object and send to pacs
alg_name = "SkullStripping"
nrrd2dcmSeg_brain = Itk2DcmSegOperator(dag=dag, 
    input_operator=get_input,
    segmentation_operator=dmrs, 
    single_label_seg_info="Brain",
    alg_name=alg_name, 
    series_description=f'{alg_name} - Brain')

dcmseg_send_brain = DcmSendOperator(dag=dag, input_operator=nrrd2dcmSeg_brain)

pdf2dcm = Pdf2DcmOperator(
    dag=dag,
    input_operator=dmrs_report,
    dicom_operator=get_input,
    pdf_title=f"CBICA AI Workbench - DeepMRSeg Report {datetime.now().strftime('%d.%m.%Y %H:%M')}",
    delete_input_on_success=False
)

dcmseg_send_pdf = DcmSendOperator(
    dag=dag,
    input_operator=pdf2dcm
    #delete_input_on_success=True
)

#this was working and sending seg object to dcm4che
#get_input >> convert >> dmrs >> nrrd2dcmSeg_brain >> dcmseg_send_brain >> clean
#get_input >> extract_metadata >> clean

get_input >> convert >> dmrs >> nrrd2dcmSeg_brain >> dcmseg_send_brain >> clean
get_input >> extract_metadata
dmrs >> dmrs_report
extract_metadata >> dmrs_report
#dmrs_report >> put_to_minio >> clean
dmrs_report >> pdf2dcm >> dcmseg_send_pdf >> clean
