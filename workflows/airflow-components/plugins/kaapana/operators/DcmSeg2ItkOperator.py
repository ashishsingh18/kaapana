from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator
from datetime import timedelta

class DcmSeg2ItkOperator(KaapanaBaseOperator):

    def __init__(self,
                 dag,
                 output_type=None,
                 seg_filter=None,
                 env_vars=None,
                 execution_timeout=timedelta(minutes=5),
                 *args, **kwargs
                 ):

        if env_vars is None:
            env_vars = {}

        envs = {
            "OUTPUT_TYPE": output_type or 'nrrd',
            "SEG_FILTER": seg_filter or '', # a bash list i.e.: 'liver aorta'
            "DCMQI_COMMAND": "segimage2itkimage",
        }

        env_vars.update(envs)

        super().__init__(
            dag=dag,
            image="dktk-jip-registry.dkfz.de/processing-external/dcmqi:1.3-vdev",
            name="dcmseg2nrrd",
            env_vars=env_vars,
            image_pull_secrets=["camic-registry"],
            execution_timeout=execution_timeout,
            ram_mem_mb=3000,
            *args, **kwargs
            )