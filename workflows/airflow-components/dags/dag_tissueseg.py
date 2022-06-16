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
#from muse.MuseOperator import MuseOperator
from tissueseg.TissueSegOperator import TissueSegOperator
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
    dag_id='tissueseg',
    default_args=args,
    schedule_interval=None
    )


                                       
get_input = LocalGetInputDataOperator(dag=dag)
convert = DcmConverterOperator(dag=dag, input_operator=get_input, output_format='nii.gz')
dmrs = DeepMRSegOperator(dag=dag, input_operator=convert)
#dmrs_muse = DeepMRSegOperator(dag=dag, input_operator=convert)
#applymask_run_muse = MuseOperator(dag=dag, input_operator=convert,mask_operator=dmrs,batch_size=4)
applymask_run_tissueseg = TissueSegOperator(dag=dag, input_operator=convert,mask_operator=dmrs,batch_size=4)

extract_metadata = LocalDcm2JsonOperator(dag=dag, input_operator=get_input, delete_private_tags=True)
#put_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[dmrs_muse], file_white_tuples=('.nrrd'))
clean = LocalWorkflowCleanerOperator(dag=dag,clean_workflow_dir=False)

#put_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[dmrs_report], file_white_tuples=('.pdf'))
#the below pipeline works and sends nrrd to minio
#get_input >> convert >> dmrs >> put_to_minio >> clean

#-----------
#convert nrrd to dicom seg object and send to pacs
# alg_name = "SkullStripping"
# nrrd2dcmSeg_brainmask = Itk2DcmSegOperator(dag=dag, 
#     input_operator=get_input,
#     segmentation_operator=dmrs, 
#     single_label_seg_info="Brain",
#     alg_name=alg_name, 
#     series_description=f'{alg_name} - Brain')

# dcmseg_send_brainmask = DcmSendOperator(dag=dag, input_operator=nrrd2dcmSeg_brainmask)

# alg_name = "Muse"
# nrrd2dcmSeg_muse = Itk2DcmSegOperator(dag=dag,
#     input_operator=get_input,
#     segmentation_operator=applymask_run_muse,
#     single_label_seg_info="Muse",
#     alg_name=alg_name,
#     series_description=f'{alg_name} - Brain')

# dcmseg_send_brainmuse = DcmSendOperator(dag=dag, input_operator=nrrd2dcmSeg_muse)

alg_name = "TissueSeg"
# nrrd2dcmSeg_tissueseg = Itk2DcmSegOperator(dag=dag,
#     input_operator=get_input,
#     segmentation_operator=applymask_run_tissueseg,
#     single_label_seg_info="TissueSeg",
#     alg_name=alg_name,
#     series_description=f'{alg_name} - Brain')
nrrd2dcmSeg_tissueseg = Itk2DcmSegOperator(dag=dag,
    input_operator=get_input,
    segmentation_operator=applymask_run_tissueseg,
    input_type="multi_label_seg",
    multi_label_seg_name=alg_name,
    alg_name=alg_name,
    series_description=f'{alg_name} - Brain')


dcmseg_send_braintissuseg = DcmSendOperator(dag=dag, input_operator=nrrd2dcmSeg_tissueseg)

dmrs_report = DeepMRSegReportOperator(
    dag=dag,
    input_operator=get_input,
    roi_operator=applymask_run_tissueseg,
    dicom_metadata_json_operator=extract_metadata)

put_to_minio = LocalMinioOperator(dag=dag, action='put', action_operators=[dmrs_report], file_white_tuples=('.pdf'))

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
#get_input >> convert >> dmrs >> nrrd2dcmSeg_brainmask >> dcmseg_send_brainmask >> clean
#get_input >> extract_metadata >> clean

#get_input >> convert >> dmrs >> nrrd2dcmSeg_brainmask >> dcmseg_send_brainmask >> clean
get_input >> convert >> dmrs
#convert >> dmrs_muse >> put_to_minio
get_input >> extract_metadata
#dmrs >> dmrs_report
#dmrs >> applymask_run_muse >> nrrd2dcmSeg_muse >> dcmseg_send_brainmuse >> clean
dmrs >> applymask_run_tissueseg >> nrrd2dcmSeg_tissueseg >> dcmseg_send_braintissuseg >> clean
extract_metadata >> dmrs_report
applymask_run_tissueseg >> dmrs_report >> put_to_minio >> clean
#dmrs_report >> put_to_minio >> clean
#dmrs_report >> pdf2dcm >> dcmseg_send_pdf >> clean
