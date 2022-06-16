from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project
from kaapana.kubetools.resources import Resources as PodResources

class MuseOperator(KaapanaBaseOperator):

    execution_timeout=timedelta(hours=5)

    def __init__(self,
                 dag,
                 mask_operator=None,
                 batch_size=None,
                 env_vars=None,
                 execution_timeout=execution_timeout,
                 *args, **kwargs
                 ):

        if env_vars is None:
            env_vars = {}

        envs = {
            "OPERATOR_IN_MASK_DIR":  ("None" if mask_operator is None else mask_operator.operator_out_dir), # directory that contains segmented mask object
            "BATCH_SIZE":  str(batch_size)
        }
        env_vars.update(envs)

        pod_resources = PodResources(request_memory=None, request_cpu=None, limit_memory=None, limit_cpu=None, limit_gpu=None)

        super().__init__(
            dag=dag,
            name='muse',
            env_vars=env_vars,
            image="{}{}/muse:0.1.2".format(default_registry, default_project),
            gpu_mem_mb=5500,
            pod_resources=pod_resources,
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            *args,
            **kwargs
        )
