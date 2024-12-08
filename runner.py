import subprocess

from config import global_config

class RunCogVideoX:

    def __init__(self):
        self.run_cogvideox()

    def run_cogvideox(self):
        
        settings = global_config
        assert settings.get_cogvideox_factory_path()
        cmd = f"accelerate launch --config_file {settings.get_cogvideox_factory_path()}/accelerate_configs/{settings.get('accelerate_config')} --gpu_ids {settings.get('gpu_ids')}  {settings.get_cogvideox_factory_path()}/training/{settings.get('training_type')}.py "
        for key, value in settings.get_all():
            if key in ["accelerate_config", "training_type", "gpu_ids", "path_to_cogvideox_factory"]:
                continue
            if not value:
                continue
            if value is False:
                continue
            if value is True:
                cmd += f"--{key} "
            else:
                cmd += f"--{key} {value} "

        print(cmd)
        subprocess.run(cmd, shell=True)