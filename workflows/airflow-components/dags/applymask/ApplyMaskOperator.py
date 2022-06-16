from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project


class ApplyMaskOperator(KaapanaBaseOperator):

    execution_timeout=timedelta(minutes=10)

    def __init__(self,
                 dag,
                 mask_operator=None,
                 env_vars=None,
                 execution_timeout=execution_timeout,
                 *args, **kwargs
                 ):

        if env_vars is None:
            env_vars = {}

        envs = {
            "OPERATOR_IN_MASK_DIR":  ("None" if mask_operator is None else mask_operator.operator_out_dir) # directory that contains segmented mask object
        }
        env_vars.update(envs)

        super().__init__(
            dag=dag,
            name='applymask',
            env_vars=env_vars,
            image="{}{}/applymask:0.1.0".format(default_registry, default_project),
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            *args,
            **kwargs
        )
