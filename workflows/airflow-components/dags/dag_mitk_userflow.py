from airflow.models import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from datetime import datetime
from mitk_userflow.MitkInputOperator import MitkInputOperator
from mitk_userflow.RunMitk import RunMitk
from kaapana.operators.DcmWebSendOperator import DcmWebSendOperator
from kaapana.operators.LocalDagTriggerOperator import LocalDagTriggerOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator


dag_info = {
    "visible": False,
}

dag_info = {
    "visible": False,
}

args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'retries': 0,
    'dag_info': dag_info,
    'retry_delay': timedelta(seconds=30000),
}

dag = DAG(
    dag_id='mitk-userflow',
    default_args=args,
    schedule_interval=None)

mitk_input = MitkInputOperator(dag=dag)
run_mitk = RunMitk(dag=dag, data_operator=mitk_input)


dcmseg_send_segmentation = DcmWebSendOperator(dag=dag, input_operator=run_mitk)
trigger_extract_meta = LocalDagTriggerOperator(dag=dag, input_operator=run_mitk, trigger_dag_id='extract-metadata')
clean = LocalWorkflowCleanerOperator(dag=dag)

mitk_input >> run_mitk >> dcmseg_send_segmentation >> clean
run_mitk >> trigger_extract_meta >> clean