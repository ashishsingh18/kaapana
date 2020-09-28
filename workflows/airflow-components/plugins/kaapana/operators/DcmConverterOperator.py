from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator
from datetime import timedelta

class DcmConverterOperator(KaapanaBaseOperator):


    def __init__(self,
                 dag,
                 output_format="nrrd",
                 env_vars=None,
                 execution_timeout=timedelta(minutes=15),
                 *args, **kwargs
                 ):

        if env_vars is None:
            env_vars = {}

        envs = {
            "CONVERTTO": output_format,
            }

        env_vars.update(envs)

        if  output_format != "nrrd" and ( output_format != "nii.gz" and output_format != "nii") :
            print(("output format %s is currently not supported!" % output_format))
            print("Dcm2nrrdOperator options: 'nrrd' or 'nii'")
            exit(1)

        super().__init__(
            dag=dag,
            image="dktk-jip-registry.dkfz.de/processing-external/mitk-fileconverter:1.1-vdev",
            name='dcm-converter',
            env_vars=env_vars,
            image_pull_secrets=["camic-registry"],
            execution_timeout=execution_timeout,
            ram_mem_mb=1000,
            *args, **kwargs
            )