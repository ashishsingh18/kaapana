from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project
from kaapana.kubetools.resources import Resources as PodResources

class Seg2RGBDicomOperator(KaapanaBaseOperator):

    execution_timeout=timedelta(minutes=60)

    def __init__(self,
                 dag,
                 mask_operator=None,
                 ref_image=None,
                 dicom_metadata_json=None,
                 series_number="901",
                 series_description="Segmentation Overlay",
                 modality=None,
                 env_vars=None,
                 execution_timeout=execution_timeout,
                 *args, **kwargs
                 ):

        if env_vars is None:
            env_vars = {}

        envs = {
            "SERIES_NUM":str(series_number),
            "SERIES_DESC":  str(series_description),
            "MODALITY": str(modality),
            "OPERATOR_IN_MASK_DIR":  ("None" if mask_operator is None else mask_operator.operator_out_dir), # directory that contains segmented mask object
            "OPERATOR_IN_DCM_JSON_DIR": dicom_metadata_json.operator_out_dir, # directory that contains input dicom metadata in json format
            "OPERATOR_IN_REFERENCE_IMAGE_DIR": ("None" if ref_image is None else ref_image.operator_out_dir) # directory that contains input reference dicom on which we want to overlay the mask
        }
        env_vars.update(envs)

        pod_resources = PodResources(request_memory=None, request_cpu=None, limit_memory=None, limit_cpu=None, limit_gpu=None)

        super().__init__(
            dag=dag,
            name='seg2rgbdicom',
            env_vars=env_vars,
            image="{}{}/seg2rgbdicom:0.1.0".format(default_registry, default_project),
            gpu_mem_mb=5500,
            pod_resources=pod_resources,
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            *args,
            **kwargs
        )
