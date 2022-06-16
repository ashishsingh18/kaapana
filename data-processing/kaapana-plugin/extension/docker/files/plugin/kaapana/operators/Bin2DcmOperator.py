import os
from datetime import timedelta
from kaapana.kubetools.volume_mount import VolumeMount
from kaapana.kubetools.volume import Volume
from kaapana.kubetools.resources import Resources as PodResources
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_platform_abbr, default_platform_version


class Bin2DcmOperator(KaapanaBaseOperator):
    execution_timeout = timedelta(minutes=10)

    def __init__(self,
                 dag,
                 dataset_info_operator=None,
                 dataset_info_operator_in_dir=None,
                 file_extensions="*.zip",
                 size_limit=100,
                 patient_id="",
                 patient_name="",
                 protocol_name="",
                 instance_name="N/A",
                 version="0.0.0",
                 manufacturer="KAAPANA",
                 manufacturer_model="bin2dcm",
                 study_description=None,
                 series_description=None,
                 study_id="bin2dcm",
                 study_uid=None,
                 name="bin2dcm",
                 env_vars={},
                 execution_timeout=execution_timeout,
                 **kwargs
                 ):

        if dataset_info_operator_in_dir is None:
            dataset_info_operator_in_dir = dataset_info_operator.operator_out_dir if dataset_info_operator is not None else ''
        
        envs = {
            "DATASET_INFO_OPERATOR_DIR": dataset_info_operator_in_dir,
            "STUDY_ID": str(study_id),
            "STUDY_UID": str(study_uid),
            "STUDY_DESCRIPTION": str(study_description),
            "SERIES_DESCRIPTION": str(series_description),
            "PATIENT_NAME": str(patient_name),
            "PATIENT_ID": str(patient_id),
            "INSTANCE_NAME": str(instance_name),
            "MANUFACTURER": str(manufacturer),
            "MANUFACTURER_MODEL": str(manufacturer_model),
            "VERSION": str(version),
            "PROTOCOL_NAME": str(protocol_name),
            "SIZE_LIMIT_MB": str(size_limit),
            "EXTENSIONS": file_extensions,
        }
        env_vars.update(envs)

        super().__init__(
            dag=dag,
            image=f"{default_registry}/bin2dcm:{default_platform_abbr}_{default_platform_version}__3.6.4",
            name=name,
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            keep_parallel_id=False,
            env_vars=env_vars,
            ram_mem_mb=5000,
            **kwargs
        )
