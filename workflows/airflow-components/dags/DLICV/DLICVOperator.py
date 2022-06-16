from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project
from kaapana.kubetools.resources import Resources as PodResources

class DLICVOperator(KaapanaBaseOperator):

    execution_timeout=timedelta(minutes=60)

    def __init__(self,
                 dag,
                 mask_operator=None,
                 batch_size=None,
                 modeldir=None,
                 env_vars=None,
                 execution_timeout=execution_timeout,
                 *args, **kwargs
                 ):

        if env_vars is None:
            env_vars = {}

        envs = {
            "MODEL_DIR":str(modeldir),
            "BATCH_SIZE":  str(batch_size)
        }
        env_vars.update(envs)

        pod_resources = PodResources(request_memory=None, request_cpu=None, limit_memory=None, limit_cpu=None, limit_gpu=None)

        super().__init__(
            dag=dag,
            name='dlicv',
            env_vars=env_vars,
            image="{}{}/dlicv:0.1.0".format(default_registry, default_project),
            gpu_mem_mb=5500,
            pod_resources=pod_resources,
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            *args,
            **kwargs
        )
