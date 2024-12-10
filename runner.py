import subprocess

from config import Config, global_config

class RunCogVideoX:

    def run_cogvideox(self, settings: Config):
        
        assert settings.get_cogvideox_factory_path()
        cmd = f"accelerate launch --config_file {settings.get_cogvideox_factory_path()}/accelerate_configs/{settings.get('accelerate_config', 'train')} --gpu_ids {settings.get('gpu_ids', 'train')}  {settings.get_cogvideox_factory_path()}/training/{settings.get('training_type', 'train')}.py "
        for key, value in settings.get_all():
            if 'train_' not in key:
                continue
            if key in ["train_accelerate_config", "train_training_type", "train_gpu_ids", "path_to_cogvideox_factory"]:
                continue
            key = key.replace('train_', '', 1)
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
    
    def run(self, settings: Config):
        
        cmd = f"torchrun --nproc_per_node={settings.get('nproc_per_node', 'prepare')} {settings.get_cogvideox_factory_path()}/training/prepare_dataset.py \
      --model_id {settings.get('model_id', 'prepare')} \
      --data_root {settings.get('data_root', 'prepare')} \
      --caption_column  {settings.get('caption_column', 'prepare')} \
      --video_column {settings.get('video_column', 'prepare')} \
      --output_dir {settings.get('output_dir', 'prepare')} \
      --height_buckets {settings.get('height_buckets', 'prepare')} \
      --width_buckets {settings.get('width_buckets', 'prepare')} \
      --frame_buckets {settings.get('frame_buckets', 'prepare')} \
      --max_num_frames {settings.get('max_num_frames', 'prepare')} \
      --max_sequence_length {settings.get('max_sequence_length', 'prepare')} \
      --target_fps {settings.get('target_fps', 'prepare')} \
      --batch_size {settings.get('batch_size', 'prepare')} "
        
        if settings.get('save_latents_and_embeddings', 'prepare') == True:
            cmd += f"--save_latents_and_embeddings "
        if settings.get('save_image_latents', 'prepare') == True:
            cmd += f"--save_image_latents "

        print(cmd)
        return subprocess.run(cmd, shell=True)