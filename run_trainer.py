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
        assert config.get('pretrained_model_name_or_path'), "pretrained_model_name_or_path required"

        parallel_backend = config.get('parallel_backend')
        parallel_cmd = ["--parallel_backend", parallel_backend,
                            "--pp_degree", config.get('pp_degree'),
                            "--dp_degree", config.get('dp_degree'),
                            "--dp_shards", config.get('dp_shards'),
                            "--cp_degree", config.get('cp_degree'),
                            "--tp_degree", config.get('tp_degree')]
        
        model_cmd = ["--model_name", config.get('model_name'), 
                     "--pretrained_model_name_or_path", config.get('pretrained_model_name_or_path'),
                     "--text_encoder_dtype", config.get('text_encoder_dtype'),
                     "--text_encoder_2_dtype", config.get('text_encoder_2_dtype'),
                     "--text_encoder_3_dtype", config.get('text_encoder_3_dtype'),
                     "--transformer_dtype", config.get('transformer_dtype'),
                     "--vae_dtype", config.get('vae_dtype')]
        if config.get('text_encoder_id'):
            model_cmd += ["--text_encoder_id", config.get('text_encoder_id')]
        if config.get('text_encoder_2_id'):
            model_cmd += ["--text_encoder_2_id", config.get('text_encoder_2_id')]
        if config.get('text_encoder_3_id'):
            model_cmd += ["--text_encoder_3_id", config.get('text_encoder_3_id')]
        if config.get('transformer_id'):
            model_cmd += ["--transformer_id", config.get('transformer_id')]
        if config.get('vae_id'):
            model_cmd += ["--vae_id", config.get('vae_id')]
        if config.get('tokenizer_id'):
            model_cmd += ["--tokenizer_id", config.get('tokenizer_id')]
        if config.get('tokenizer_2_id'):
            model_cmd += ["--tokenizer_2_id", config.get('tokenizer_2_id')]
        if config.get('tokenizer_3_id'):
            model_cmd += ["--tokenizer_3_id", config.get('tokenizer_3_id')]

        if config.get('layerwise_upcasting_modules') != 'none':
            model_cmd +=["--layerwise_upcasting_modules", config.get('layerwise_upcasting_modules'),
            "--layerwise_upcasting_storage_dtype", config.get('layerwise_upcasting_storage_dtype'),
            "--layerwise_upcasting_skip_modules_pattern", config.get('layerwise_upcasting_skip_modules_pattern')]

        dataset_cmd = ["--dataset_config", config.get('dataset_config'),
                    "--caption_dropout_p", config.get('caption_dropout_p'),
                    "--caption_dropout_technique", config.get('caption_dropout_technique'),
                    "--enable_precomputation" if config.get('enable_precomputation') else '',
                    "--precomputation_items", config.get('precomputation_items'),
                    "--precomputation_dir" if config.get('precomputation_dir') else '',
                    "--precomputation_once" if config.get('precomputation_once') else '']

        dataloader_cmd = ["--dataloader_num_workers", config.get('dataloader_num_workers')]

        # TODO: seems to have changed, need full options
        #diffusion_cmd = [config.get('diffusion_options')]

        training_cmd = ["--training_type", config.get('training_type'),
                "--seed", config.get('seed'),
                "--batch_size", config.get('batch_size'),
                "--train_steps", config.get('train_steps')]
        training_cmd += config.get('target_modules').split(' ')
        training_cmd += ["--gradient_accumulation_steps", config.get('gradient_accumulation_steps'),
                '--gradient_checkpointing' if config.get('gradient_checkpointing') else '',
                "--checkpointing_steps", config.get('checkpointing_steps'),
                "--checkpointing_limit", config.get('checkpointing_limit'),
                '--enable_slicing' if config.get('enable_slicing') else '',
                '--enable_tiling' if config.get('enable_tiling') else '']
        if config.get('enable_model_cpu_offload'):
            training_cmd += ["--enable_model_cpu_offload"]

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

        validation_cmd = ["--validation_dataset_file" if config.get('validation_dataset_file') else '',
                  "--num_validation_videos", config.get('num_validation_videos'),
                  "--validation_steps", config.get('validation_steps')]
        
        control_cmd = ["--rank", config.get('rank'),
                "--lora_alpha", config.get('lora_alpha'),
                "--control_type", config.get('control_type'),
                "--frame_conditioning_index", config.get('frame_conditioning_index'),
                "--frame_conditioning_type", config.get('frame_conditioning_type')]

        miscellaneous_cmd = ["--tracker_name", config.get('tracker_name'),
                     "--output_dir", config.get('output_dir'),
                     "--nccl_timeout", config.get('nccl_timeout'),
                     "--report_to", config.get('report_to')]
        
        pre_command = ''
        num_gpus = config.get('num_gpus')
        address = config.get('master_address')
        port = config.get('master_port')
        if parallel_backend == 'accelerate':
            os.environ['WORLD_SIZE'] = f'{num_gpus}'
            os.environ['RANK'] = config.get('gpu_ids')
            os.environ['MASTER_ADDR'] = address
            os.environ['MASTER_PORT'] = f'{port}'
            pre_command = ["accelerate", "launch", "--config_file", f"{finetrainers_path}/accelerate_configs/{config.get('accelerate_config')}", "--gpu_ids", config.get('gpu_ids')]
        elif parallel_backend == 'ptd':
            pre_command = ["torchrun", "--standalone", "--nnodes", num_gpus, "--nproc_per_node", config.get('nproc_per_node'), "--rdzv_backend", "c10d", "--rdzv_endpoint", f"{address}:{port}"]
        cmd = pre_command + [f"{finetrainers_path}/train.py"] + parallel_cmd + model_cmd + dataset_cmd + dataloader_cmd + training_cmd + optimizer_cmd + validation_cmd + miscellaneous_cmd + control_cmd
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