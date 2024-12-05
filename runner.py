import subprocess


class RunCogVideoX:

    def __init__(self, cogvideo_path, settings):
        self.run_cogvideox(cogvideo_path, settings)

    def run_cogvideox(self, cogvideo_path, settings):

        cmd = f"accelerate launch --config_file {settings['accelerate_config']} --gpu_ids {settings['gpu_ids']}  {cogvideo_path}training/{settings['training_type']} "
        for key, value in settings.items():
            if key in ["accelerate_config", "training_type", "gpu_ids"]:
                continue
            if value is False:
                continue
            if value is True:
                cmd += f"--{key} "
            cmd += f"--{key} {value} "

        print(cmd)

        subprocess.run(cmd, shell=True)