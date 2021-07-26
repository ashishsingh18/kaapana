from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project


class DeepMRSegReportOperator(KaapanaBaseOperator):

    execution_timeout=timedelta(minutes=10)

    def __init__(self,
                 dag,
                 brainmask_operator=None,
                 icv_operator=None,
                 roi_operator=None,
                 dicom_metadata_json_operator=None,
                 env_vars=None,
                 execution_timeout=execution_timeout,
                 *args, **kwargs
                 ):

        if env_vars is None:
            env_vars = {}

        envs = {
            "OPERATOR_IN_DIR_BMASK":  ("None" if brainmask_operator is None else brainmask_operator.operator_out_dir), # directory that contains segmented brain mask object
            "OPERATOR_IN_DIR_ICV":  ("None" if icv_operator is None else icv_operator.operator_out_dir), # directory that contains segmented ICV object
            "OPERATOR_IN_DIR_ROI":  ("None" if roi_operator is None else roi_operator.operator_out_dir), # directory that contains segmented roi object
            "OPERATOR_IN_DCM_METADATA_DIR":  dicom_metadata_json_operator.operator_out_dir # directory that contains input dicom metadata in json format
        }
        env_vars.update(envs)

        super().__init__(
            dag=dag,
            name='deepmrsegreport',
            env_vars=env_vars,
            image="{}{}/deepmrseg-report:0.1.1".format(default_registry, default_project),
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            *args,
            **kwargs
        )
