from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project


class MuseROISubsetCreatorOperator(KaapanaBaseOperator):

    def __init__(self,
                 dag,
                 execution_timeout=timedelta(seconds=60),
                 *args, **kwargs
                 ):

        super().__init__(
            dag=dag,
            name='MuseROISubsetCreator',
            image="{}{}/muse-roi-subset-creator:0.1.1".format(default_registry, default_project),
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            *args,
            **kwargs
        )
