from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project
from datetime import timedelta

class ExtractScanparameterOperator(KaapanaBaseOperator):

    def __init__(self,
                 dag,
                 execution_timeout=timedelta(minutes=120),
                 **kwargs
                 ):

        super().__init__(
            dag=dag,
            image=f"{default_registry}/scanparam2json:0.1.0",
            name='extract-scanparam',
            image_pull_policy="Always",
            image_pull_secrets=['registry-secret'],
            execution_timeout=execution_timeout,
            **kwargs
        )