import os
import re

class TrainerValidator:

    def __init__(self, config):
        self.config = config

    def validate(self):
        required_settings = [
            'path_to_finetrainers',
            'accelerate_config',
            'batch_size',
            'beta1',
            'beta2',
            'caption_dropout_p',
            'checkpointing_limit',
            'checkpointing_steps',
            'dataloader_num_workers',
            'epsilon',
            'gpu_ids',
            'gradient_accumulation_steps',
            'lora_alpha',
            'lr',
            'lr_num_cycles',
            'lr_scheduler',
            'lr_warmup_steps',
            'max_grad_norm',
            'model_name',
            'nccl_timeout',
            'optimizer',
            'pretrained_model_name_or_path',
            'rank',
            'seed',
            'target_modules',
            'train_steps',
            'training_type',
            'validation_steps',
            'weight_decay'
        ]

        for setting in required_settings:
            if not self.config.get(setting) and self.config.get(setting) != 0:
                raise ValueError(f"{setting} is required")
            
        self.validate_finetrainers_path()

    def validate_finetrainers_path(self):
        train_script_path = os.path.join(self.config.get('path_to_finetrainers'), 'train.py')
        if not os.path.isfile(train_script_path):
            raise ValueError(f"train.py does not exist at {self.config.get('path_to_finetrainers')}")