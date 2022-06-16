from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project


class SortDicomOperator(KaapanaBaseOperator):

    def __init__(self,
                 dag,
                 series_description=None,
                 env_vars=None,
                 execution_timeout=timedelta(seconds=30),
                 *args, **kwargs
                 ):

        if env_vars is None:
            env_vars = {}

        envs = {
            "SERIES_DESC":  str(series_description)
        }
        env_vars.update(envs)

        super().__init__(
            dag=dag,
            name='sortdicom',
            env_vars=env_vars,
            image="{}{}/sort-dicom:0.1.0".format(default_registry, default_project),
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            *args,
            **kwargs
        )
