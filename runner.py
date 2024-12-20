import subprocess

from config import Config

class RunCogVideoX:

    def run_cogvideox(self, settings: Config, cogvideox_factory_path: str):
        
        cmd = f"accelerate launch --config_file {cogvideox_factory_path}/accelerate_configs/{settings.get('accelerate_config')} --gpu_ids {settings.get('gpu_ids')}  {cogvideox_factory_path}/training/cogvideox/{settings.get('training_type')}.py "
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
        return subprocess.run(cmd, shell=True)

class RunPrepareDataset:
    
    def run(self, settings: Config, cogvideox_factory_path: str):
        
        cmd = f"torchrun --nproc_per_node={settings.get('nproc_per_node')} {cogvideox_factory_path}/training/cogvideox/prepare_dataset.py \
      --model_id {settings.get('model_id')} \
      --data_root {settings.get('data_root')} \
      --caption_column  {settings.get('caption_column')} \
      --video_column {settings.get('video_column')} \
      --output_dir {settings.get('output_dir')} \
      --height_buckets {settings.get('height_buckets')} \
      --width_buckets {settings.get('width_buckets')} \
      --frame_buckets {settings.get('frame_buckets')} \
      --max_num_frames {settings.get('max_num_frames')} \
      --max_sequence_length {settings.get('max_sequence_length')} \
      --target_fps {settings.get('target_fps')} \
      --batch_size {settings.get('batch_size')} "
        
        if settings.get('save_latents_and_embeddings') == True:
            cmd += f"--save_latents_and_embeddings "
        if settings.get('save_image_latents') == True:
            cmd += f"--save_image_latents "

        print(cmd)
        return subprocess.run(cmd, shell=True)