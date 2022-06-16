import os
import glob
from datetime import timedelta

from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_platform_abbr, default_platform_version

class NnUnetNotebookOperator(KaapanaBaseOperator):

    def __init__(self,
                 dag,
                 name='nnunet-notebook-operator',
                 execution_timeout=timedelta(minutes=20),
                 *args, **kwargs
                 ):

        super().__init__(
            dag=dag,
            name=name,
            image=f"{default_registry}/nnunet-gpu:{default_platform_abbr}_{default_platform_version}__03-22",
            image_pull_secrets=["registry-secret"],
            cmds=["/bin/bash"],
            execution_timeout=execution_timeout,
            ram_mem_mb=1000,
            ram_mem_mb_lmt=3000,
            *args, **kwargs
        )