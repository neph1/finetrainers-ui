import os
import re

class TrainerValidator:

    def __init__(self, config):
        self.config = config

    def validate(self):
        self.validate_finetrainers_path()
        self.validate_accelerate_config()
        self.validate_batch_size()
        self.validate_beta1()
        self.validate_beta2()
        self.validate_caption_column()
        self.validate_caption_dropout_p()
        self.validate_checkpointing_limit()
        self.validate_checkpointing_steps()
        self.validate_data_root()
        self.validate_dataloader_num_workers()
        self.validate_epsilon()
        self.validate_gpu_ids()
        self.validate_gradient_accumulation_steps()
        self.validate_id_token()
        self.validate_lora_alpha()
        self.validate_lr()
        self.validate_lr_num_cycles()
        self.validate_lr_scheduler()
        self.validate_lr_warmup_steps()
        self.validate_max_grad_norm()
        self.validate_mixed_precision()
        self.validate_model_name()
        self.validate_nccl_timeout()
        self.validate_optimizer()
        self.validate_pretrained_model_name_or_path()
        self.validate_rank()
        self.validate_seed()
        self.validate_target_modules()
        self.validate_tracker_name()
        self.validate_train_steps()
        self.validate_training_type()
        self.validate_validation_steps()
        self.validate_video_column()
        self.validate_video_resolution_buckets()
        self.validate_weight_decay()

    def validate_finetrainers_path(self):
        if not isinstance(self.config.get('finetrainers_path'), str) or not self.config.get('finetrainers_path'):
            raise ValueError("finetrainers_path must be a string")
        train_script_path = os.path.join(self.config.get('finetrainers_path'), 'train.py')
        if not os.path.isfile(train_script_path):
            raise ValueError(f"train.py does not exist at {self.config.get('finetrainers_path')}")
        
    def validate_accelerate_config(self):
        if not isinstance(self.config.get('accelerate_config'), str) or not self.config.get('accelerate_config'):
            raise ValueError("accelerate_config must be a string")

    def validate_batch_size(self):
        if not isinstance(self.config.get('batch_size'), int):
            raise ValueError("batch_size must be an integer")

    def validate_beta1(self):
        if not isinstance(self.config.get('beta1'), float):
            raise ValueError("beta1 must be a float")

    def validate_beta2(self):
        if not isinstance(self.config.get('beta2'), float):
            raise ValueError("beta2 must be a float")

    def validate_caption_column(self):
        data_root = self.config.get('data_root')
        caption_column = self.config.get('caption_column')
        if not isinstance(caption_column, str) or not caption_column:
            raise ValueError("caption_column must be a string")
        if data_root and caption_column:
            file_path = os.path.join(data_root, caption_column)
            if not os.path.isfile(file_path):
                raise ValueError(f"File {caption_column} does not exist at {data_root}")

    def validate_caption_dropout_p(self):
        if not isinstance(self.config.get('caption_dropout_p'), float):
            raise ValueError("caption_dropout_p must be a float")

    def validate_checkpointing_limit(self):
        if not isinstance(self.config.get('checkpointing_limit'), int):
            raise ValueError("checkpointing_limit must be an integer")

    def validate_checkpointing_steps(self):
        if not isinstance(self.config.get('checkpointing_steps'), int):
            raise ValueError("checkpointing_steps must be an integer")

    def validate_data_root(self):
        data_root = self.config.get('data_root')
        if not isinstance(data_root, str) or not data_root:
            raise ValueError("data_root must be a string")
        if data_root and not os.path.isdir(data_root):
            raise ValueError(f"data_root path {data_root} does not exist")

    def validate_dataloader_num_workers(self):
        if not isinstance(self.config.get('dataloader_num_workers'), int):
            raise ValueError("dataloader_num_workers must be an integer")

    def validate_epsilon(self):
        if not isinstance(self.config.get('epsilon'), float):
            raise ValueError("epsilon must be a float")

    def validate_gpu_ids(self):
        if not isinstance(self.config.get('gpu_ids'), str) or not self.config.get('gpu_ids'):
            raise ValueError("gpu_ids must be a string")

    def validate_gradient_accumulation_steps(self):
        if not isinstance(self.config.get('gradient_accumulation_steps'), int):
            raise ValueError("gradient_accumulation_steps must be an integer")

    def validate_id_token(self):
        if not isinstance(self.config.get('id_token'), str) or not self.config.get('id_token'):
            raise ValueError("id_token must be a string")

    def validate_lora_alpha(self):
        if not isinstance(self.config.get('lora_alpha'), int):
            raise ValueError("lora_alpha must be an integer")

    def validate_lr(self):
        if not isinstance(self.config.get('lr'), float):
            raise ValueError("lr must be a float")

    def validate_lr_num_cycles(self):
        if not isinstance(self.config.get('lr_num_cycles'), int):
            raise ValueError("lr_num_cycles must be an integer")

    def validate_lr_scheduler(self):
        if not isinstance(self.config.get('lr_scheduler'), str) or not self.config.get('lr_scheduler'):
            raise ValueError("lr_scheduler must be a string")

    def validate_lr_warmup_steps(self):
        if not isinstance(self.config.get('lr_warmup_steps'), int):
            raise ValueError("lr_warmup_steps must be an integer")

    def validate_max_grad_norm(self):
        if not isinstance(self.config.get('max_grad_norm'), float):
            raise ValueError("max_grad_norm must be a float")

    def validate_mixed_precision(self):
        if not isinstance(self.config.get('mixed_precision'), str) or not self.config.get('mixed_precision'):
            raise ValueError("mixed_precision must be a string")

    def validate_model_name(self):
        if not isinstance(self.config.get('model_name'), str) or not self.config.get('model_name'):
            raise ValueError("model_name must be a string")

    def validate_nccl_timeout(self):
        if not isinstance(self.config.get('nccl_timeout'), int):
            raise ValueError("nccl_timeout must be an integer")

    def validate_optimizer(self):
        if not isinstance(self.config.get('optimizer'), str) or not self.config.get('optimizer'):
            raise ValueError("optimizer must be a string")

    def validate_pretrained_model_name_or_path(self):
        if not isinstance(self.config.get('pretrained_model_name_or_path'), str):
            raise ValueError("pretrained_model_name_or_path must be set")

    def validate_rank(self):
        if not isinstance(self.config.get('rank'), int):
            raise ValueError("rank must be an integer")

    def validate_seed(self):
        if not isinstance(self.config.get('seed'), int):
            raise ValueError("seed must be an integer")

    def validate_target_modules(self):
        if not isinstance(self.config.get('target_modules'), str) or not self.config.get('target_modules'):
            raise ValueError("target_modules must be a string")

    def validate_tracker_name(self):
        if not isinstance(self.config.get('tracker_name'), str) or not self.config.get('tracker_name'):
            raise ValueError("tracker_name must be a string")

    def validate_train_steps(self):
        if not isinstance(self.config.get('train_steps'), int):
            raise ValueError("train_steps must be an integer")

    def validate_training_type(self):
        if not isinstance(self.config.get('training_type'), str) or not self.config.get('training_type'):
            raise ValueError("training_type must be a string")

    def validate_validation_steps(self):
        if not isinstance(self.config.get('validation_steps'), int):
            raise ValueError("validation_steps must be an integer")

    def validate_video_column(self):
        if not isinstance(self.config.get('video_column'), str) or not self.config.get('video_column'):
            raise ValueError("video_column must be a string")
        
        data_root = self.config.get('data_root')
        video_column = self.config.get('video_column')
        if data_root and video_column:
            file_path = os.path.join(data_root, video_column)
            if not os.path.isfile(file_path):
                raise ValueError(f"File {video_column} does not exist at {data_root}")


    def validate_video_resolution_buckets(self):
        buckets = self.config.get('video_resolution_buckets')
        if not isinstance(buckets, str):
            raise ValueError("video_resolution_buckets must be a string")
        split_buckets =  buckets.split(' ')
        for bucket in split_buckets:
            if not isinstance(bucket, str) or not re.match(r'^\d+x\d+x\d+$', bucket):
                raise ValueError(f"Each bucket must have the format '<frames>x<height>x<width>', but got {bucket}")

    def validate_weight_decay(self):
        if not isinstance(self.config.get('weight_decay'), float):
            raise ValueError("weight_decay must be a float")