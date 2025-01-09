import os
import signal
import subprocess

import psutil

from config import Config

class RunTrainer:

    def __init__(self):
        self.running = False
        self.process = None
        pass

    def run(self, config: Config, finetrainers_path: str, log_file: str):

        assert finetrainers_path, "Path to finetrainers is required"
        assert config.get('data_root'), "Data root required"
        assert config.get('pretrained_model_name_or_path'), "pretrained_model_name_or_path required"

        model_cmd = ["--model_name", config.get('model_name'), 
                     "--pretrained_model_name_or_path", config.get('pretrained_model_name_or_path')]

        dataset_cmd = ["--data_root", config.get('data_root'),
                   "--video_column", config.get('video_column'),
                   "--caption_column", config.get('caption_column'),
                   "--id_token", config.get('id_token'),
                   "--video_resolution_buckets"]
        dataset_cmd += config.get('video_resolution_buckets').split(' ')
        dataset_cmd += ["--caption_dropout_p", config.get('caption_dropout_p'),
                   "--caption_dropout_technique", config.get('caption_dropout_technique'),
                   "--text_encoder_dtype", config.get('text_encoder_dtype'),
                   "--text_encoder_2_dtype", config.get('text_encoder_2_dtype'),
                   "--text_encoder_3_dtype", config.get('text_encoder_3_dtype'),
                   "--vae_dtype", config.get('vae_dtype'),
                   '--precompute_conditions' if config.get('precompute_conditions') else '']

        dataloader_cmd = ["--dataloader_num_workers", config.get('dataloader_num_workers')]

        # Diffusion arguments TODO: replace later
        diffusion_cmd = [config.get('diffusion_options')]

        training_cmd = ["--training_type", config.get('training_type'),
                "--seed", config.get('seed'),
                "--mixed_precision", config.get('mixed_precision'),
                "--batch_size", config.get('batch_size'),
                "--train_steps", config.get('train_steps'),
                "--rank", config.get('rank'),
                "--lora_alpha", config.get('lora_alpha'),
                "--target_modules"]
        training_cmd += config.get('target_modules').split(' ')
        training_cmd += ["--gradient_accumulation_steps", config.get('gradient_accumulation_steps'),
                '--gradient_checkpointing' if config.get('gradient_checkpointing') else '',
                "--checkpointing_steps", config.get('checkpointing_steps'),
                "--checkpointing_limit", config.get('checkpointing_limit'),
                '--enable_slicing' if config.get('enable_slicing') else '',
                '--enable_tiling' if config.get('enable_tiling') else '']

        if config.get('resume_from_checkpoint'):
            training_cmd += ["--resume_from_checkpoint", config.get('resume_from_checkpoint')]

        optimizer_cmd = ["--optimizer", config.get('optimizer'),
                 "--lr", config.get('lr'),
                 "--lr_scheduler", config.get('lr_scheduler'),
                 "--lr_warmup_steps", config.get('lr_warmup_steps'),
                 "--lr_num_cycles", config.get('lr_num_cycles'),
                 "--beta1", config.get('beta1'),
                 "--beta2", config.get('beta2'),
                 "--weight_decay", config.get('weight_decay'),
                 "--epsilon", config.get('epsilon'),
                 "--max_grad_norm", config.get('max_grad_norm'),
                 '--use_8bit_bnb' if config.get('use_8bit_bnb') else '']

        validation_cmd = ["--validation_prompts" if config.get('validation_prompts') else '', config.get('validation_prompts') or '',
                  "--num_validation_videos", config.get('num_validation_videos'),
                  "--validation_steps", config.get('validation_steps')]

        miscellaneous_cmd = ["--tracker_name", config.get('tracker_name'),
                     "--output_dir", config.get('output_dir'),
                     "--nccl_timeout", config.get('nccl_timeout'),
                     "--report_to", config.get('report_to')]
        accelerate_cmd = ["accelerate", "launch", "--config_file", f"{finetrainers_path}/accelerate_configs/{config.get('accelerate_config')}", "--gpu_ids", config.get('gpu_ids')]
        cmd = accelerate_cmd + [f"{finetrainers_path}/train.py"] + model_cmd + dataset_cmd + dataloader_cmd + diffusion_cmd + training_cmd + optimizer_cmd + validation_cmd + miscellaneous_cmd
        fixed_cmd = []
        for i in range(len(cmd)):
            if cmd[i] != '':
                fixed_cmd.append(f"{cmd[i]}")
        print(' '.join(fixed_cmd))
        self.running = True
        with open(log_file, "w") as output_file:
            self.process = subprocess.Popen(fixed_cmd, shell=False, stdout=output_file, stderr=output_file, text=True, preexec_fn=os.setsid)
            self.process.communicate()
            return self.process
            
        return "Unknown result"
    
    def stop(self):
        try:
            self.running = False
            if self.process:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                self.terminate_process_tree(self.process.pid)
        except Exception as e:
            return f"Error stopping training: {e}"
        finally:
            self.process.wait()
        return "Training forcibly stopped"
    
    def terminate_process_tree(pid):
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)  # Get child processes
            for child in children:
                child.terminate()
            parent.terminate()
        except psutil.NoSuchProcess:
            pass