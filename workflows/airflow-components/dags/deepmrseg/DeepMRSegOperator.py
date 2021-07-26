from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project
from kaapana.kubetools.resources import Resources as PodResources

class DeepMRSegOperator(KaapanaBaseOperator):

    execution_timeout=timedelta(minutes=30)

    def __init__(self,
                 dag,
                 execution_timeout=execution_timeout,
                 *args, **kwargs
                 ):

        pod_resources = PodResources(request_memory=None, request_cpu=None, limit_memory=None, limit_cpu=None, limit_gpu=None)

        super().__init__(
            dag=dag,
            name='deepmrseg',
            image="{}{}/deepmrseg:0.1.0".format(default_registry, default_project),
            gpu_mem_mb=5500,
            pod_resources=pod_resources,
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            *args,
            **kwargs
        )
