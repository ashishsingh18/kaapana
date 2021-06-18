from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project


class DeepMRSegOperator(KaapanaBaseOperator):

    execution_timeout=timedelta(minutes=30),

    def __init__(self,
                 dag,
                 execution_timeout=execution_timeout,
                 *args, **kwargs
                 ):

        super().__init__(
            dag=dag,
            name='deepmrseg',
            image="{}{}/deepmrseg:0.1.0".format(default_registry, default_project),
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            *args,
            **kwargs
        )
