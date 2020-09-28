from kaapana.kubetools.volume_mount import VolumeMount
from kaapana.kubetools.volume import Volume
from kaapana.kubetools.resources import Resources as PodResources

from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator
from datetime import timedelta
import os


class GetTaskModelOperator(KaapanaBaseOperator):
    execution_timeout = timedelta(minutes=120)

    def __init__(self,
                 dag,
                 task_id=None,
                 env_vars={},
                 execution_timeout=execution_timeout,
                 *args,
                 **kwargs
                 ):

        envs = {
            "MODELDIR": "/models",
        }
        env_vars.update(envs)

        if task_id is not None:
            env_vars["TASK"] = task_id

        data_dir = os.getenv('DATADIR', "")
        models_dir = os.path.join(os.path.dirname(data_dir), "models")

        volume_mounts = []
        volumes = []

        volume_mounts.append(VolumeMount(
            'models', mount_path='/models', sub_path=None, read_only=False))
        volume_config = {
            'hostPath':
            {
                'type': 'DirectoryOrCreate',
                'path': models_dir
            }
        }
        volumes.append(Volume(name='models', configs=volume_config))

        super(GetTaskModelOperator, self).__init__(
            dag=dag,
            image="dktk-jip-registry.dkfz.de/kaapana/nnunet-get-models:0.1-vdev",
            name="get-task-model",
            image_pull_secrets=["camic-registry"],
            volumes=volumes,
            volume_mounts=volume_mounts,
            execution_timeout=execution_timeout,
            env_vars=env_vars,
            ram_mem_mb=50,
            *args,
            **kwargs
        )