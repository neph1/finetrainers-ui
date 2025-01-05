import os
import pytest
from unittest.mock import patch

from trainer_config_validator import TrainerValidator

@pytest.fixture
def valid_config():
    return {
        'finetrainers_path': '/path/to/finetrainers',
        'accelerate_config': 'config1',
        'batch_size': 32,
        'beta1': 0.9,
        'beta2': 0.999,
        'caption_column': 'captions.txt',
        'caption_dropout_p': 0.1,
        'checkpointing_limit': 5,
        'checkpointing_steps': 1000,
        'data_root': '/path/to/data',
        'dataloader_num_workers': 4,
        'epsilon': 1e-8,
        'gpu_ids': '0,1',
        'gradient_accumulation_steps': 2,
        'gradient_checkpointing': True,
        'id_token': 'token123',
        'lora_alpha': 128,
        'lr': 0.001,
        'lr_num_cycles': 10,
        'lr_scheduler': 'scheduler1',
        'lr_warmup_steps': 500,
        'max_grad_norm': 1.0,
        'mixed_precision': 'fp16',
        'model_name': 'model_v1',
        'nccl_timeout': 60,
        'optimizer': 'adam',
        'pretrained_model_name_or_path': 'pretrained_model',
        'rank': 0,
        'seed': 42,
        'target_modules': 'module1',
        'tracker_name': 'tracker',
        'train_steps': 10000,
        'training_type': 'type1',
        'validation_steps': 100,
        'video_column': 'videos.txt',
        'video_resolution_buckets': '24x480x720',
        'weight_decay': 0.01
    }

@pytest.fixture
def trainer_validator(valid_config):
    return TrainerValidator(valid_config)

def test_valid_config(valid_config):
    trainer_validator = TrainerValidator(valid_config)
    with patch('os.path.isfile', return_value=True), patch('os.path.exists', return_value=True), patch('os.path.isdir', return_value=True):
        trainer_validator.validate()

def test_validate_finetrainers_path_invalid(trainer_validator):
    trainer_validator.config['finetrainers_path'] = 123
    with pytest.raises(ValueError, match="finetrainers_path must be a string"):
        trainer_validator.validate_finetrainers_path()

def test_validate_finetrainers_path_valid(trainer_validator):
    with patch('os.path.isfile', return_value=True):
        trainer_validator.config['finetrainers_path'] = '/path/to/finetrainers'
        trainer_validator.validate_finetrainers_path()

def test_validate_accelerate_config_invalid(trainer_validator):
    trainer_validator.config['accelerate_config'] = []
    with pytest.raises(ValueError, match="accelerate_config must be a string"):
        trainer_validator.validate_accelerate_config()

def test_validate_batch_size_invalid(trainer_validator):
    trainer_validator.config['batch_size'] = 'not_an_int'
    with pytest.raises(ValueError, match="batch_size must be an integer"):
        trainer_validator.validate_batch_size()

def test_validate_beta1_invalid(trainer_validator):
    trainer_validator.config['beta1'] = 'not_a_float'
    with pytest.raises(ValueError, match="beta1 must be a float"):
        trainer_validator.validate_beta1()

def test_validate_beta2_invalid(trainer_validator):
    trainer_validator.config['beta2'] = 'not_a_float'
    with pytest.raises(ValueError, match="beta2 must be a float"):
        trainer_validator.validate_beta2()

def test_validate_caption_column_invalid(trainer_validator):
    trainer_validator.config['caption_column'] = 123
    with pytest.raises(ValueError, match="caption_column must be a string"):
        trainer_validator.validate_caption_column()

def test_validate_caption_dropout_p_invalid(trainer_validator):
    trainer_validator.config['caption_dropout_p'] = 'not_a_float'
    with pytest.raises(ValueError, match="caption_dropout_p must be a float"):
        trainer_validator.validate_caption_dropout_p()

def test_validate_checkpointing_limit_invalid(trainer_validator):
    trainer_validator.config['checkpointing_limit'] = 'not_an_int'
    with pytest.raises(ValueError, match="checkpointing_limit must be an integer"):
        trainer_validator.validate_checkpointing_limit()

def test_validate_checkpointing_steps_invalid(trainer_validator):
    trainer_validator.config['checkpointing_steps'] = 'not_an_int'
    with pytest.raises(ValueError, match="checkpointing_steps must be an integer"):
        trainer_validator.validate_checkpointing_steps()

def test_validate_data_root_invalid(trainer_validator):
    trainer_validator.config['data_root'] = '/invalid/path'
    with pytest.raises(ValueError, match="data_root path /invalid/path does not exist"):
        trainer_validator.validate_data_root()

def test_validate_data_root_valid(trainer_validator):
    with patch('os.path.exists', return_value=True), patch('os.path.isdir', return_value=True):
        trainer_validator.config['data_root'] = '/path/to/data'
        trainer_validator.validate_data_root()

def test_validate_dataloader_num_workers_invalid(trainer_validator):
    trainer_validator.config['dataloader_num_workers'] = 'not_an_int'
    with pytest.raises(ValueError, match="dataloader_num_workers must be an integer"):
        trainer_validator.validate_dataloader_num_workers()

def test_validate_epsilon_invalid(trainer_validator):
    trainer_validator.config['epsilon'] = 'not_a_float'
    with pytest.raises(ValueError, match="epsilon must be a float"):
        trainer_validator.validate_epsilon()

def test_validate_gpu_ids_invalid(trainer_validator):
    trainer_validator.config['gpu_ids'] = 123
    with pytest.raises(ValueError, match="gpu_ids must be a string"):
        trainer_validator.validate_gpu_ids()

def test_validate_gradient_accumulation_steps_invalid(trainer_validator):
    trainer_validator.config['gradient_accumulation_steps'] = 'not_an_int'
    with pytest.raises(ValueError, match="gradient_accumulation_steps must be an integer"):
        trainer_validator.validate_gradient_accumulation_steps()

def test_validate_id_token_invalid(trainer_validator):
    trainer_validator.config['id_token'] = 123
    with pytest.raises(ValueError, match="id_token must be a string"):
        trainer_validator.validate_id_token()

def test_validate_lora_alpha_invalid(trainer_validator):
    trainer_validator.config['lora_alpha'] = 'not_an_int'
    with pytest.raises(ValueError, match="lora_alpha must be an integer"):
        trainer_validator.validate_lora_alpha()

def test_validate_lr_invalid(trainer_validator):
    trainer_validator.config['lr'] = 'not_a_float'
    with pytest.raises(ValueError, match="lr must be a float"):
        trainer_validator.validate_lr()

def test_validate_lr_num_cycles_invalid(trainer_validator):
    trainer_validator.config['lr_num_cycles'] = 'not_an_int'
    with pytest.raises(ValueError, match="lr_num_cycles must be an integer"):
        trainer_validator.validate_lr_num_cycles()

def test_validate_lr_scheduler_invalid(trainer_validator):
    trainer_validator.config['lr_scheduler'] = ''
    with pytest.raises(ValueError, match="lr_scheduler must be a string"):
        trainer_validator.validate_lr_scheduler()

def test_validate_lr_warmup_steps_invalid(trainer_validator):
    trainer_validator.config['lr_warmup_steps'] = 'not_an_int'
    with pytest.raises(ValueError, match="lr_warmup_steps must be an integer"):
        trainer_validator.validate_lr_warmup_steps()

def test_validate_max_grad_norm_invalid(trainer_validator):
    trainer_validator.config['max_grad_norm'] = 'not_a_float'
    with pytest.raises(ValueError, match="max_grad_norm must be a float"):
        trainer_validator.validate_max_grad_norm()

def test_validate_mixed_precision_invalid(trainer_validator):
    trainer_validator.config['mixed_precision'] = 123
    with pytest.raises(ValueError, match="mixed_precision must be a string"):
        trainer_validator.validate_mixed_precision()

def test_validate_model_name_invalid(trainer_validator):
    trainer_validator.config['model_name'] = 123
    with pytest.raises(ValueError, match="model_name must be a string"):
        trainer_validator.validate_model_name()

def test_validate_nccl_timeout_invalid(trainer_validator):
    trainer_validator.config['nccl_timeout'] = 'not_an_int'
    with pytest.raises(ValueError, match="nccl_timeout must be an integer"):
        trainer_validator.validate_nccl_timeout()

def test_validate_optimizer_invalid(trainer_validator):
    trainer_validator.config['optimizer'] = 123
    with pytest.raises(ValueError, match="optimizer must be a string"):
        trainer_validator.validate_optimizer()

def test_validate_pretrained_model_name_or_path_invalid(trainer_validator):
    trainer_validator.config['pretrained_model_name_or_path'] = 123
    with pytest.raises(ValueError, match="pretrained_model_name_or_path must be set"):
        trainer_validator.validate_pretrained_model_name_or_path()

def test_validate_rank_invalid(trainer_validator):
    trainer_validator.config['rank'] = 'not_an_int'
    with pytest.raises(ValueError, match="rank must be an integer"):
        trainer_validator.validate_rank()

def test_validate_seed_invalid(trainer_validator):
    trainer_validator.config['seed'] = 'not_an_int'
    with pytest.raises(ValueError, match="seed must be an integer"):
        trainer_validator.validate_seed()

def test_validate_target_modules_invalid(trainer_validator):
    trainer_validator.config['target_modules'] = 123
    with pytest.raises(ValueError, match="target_modules must be a string"):
        trainer_validator.validate_target_modules()

def test_validate_tracker_name_invalid(trainer_validator):
    trainer_validator.config['tracker_name'] = 123
    with pytest.raises(ValueError, match="tracker_name must be a string"):
        trainer_validator.validate_tracker_name()

def test_validate_train_steps_invalid(trainer_validator):
    trainer_validator.config['train_steps'] = 'not_an_int'
    with pytest.raises(ValueError, match="train_steps must be an integer"):
        trainer_validator.validate_train_steps()

def test_validate_training_type_invalid(trainer_validator):
    trainer_validator.config['training_type'] = 123
    with pytest.raises(ValueError, match="training_type must be a string"):
        trainer_validator.validate_training_type()

def test_validate_validation_steps_invalid(trainer_validator):
    trainer_validator.config['validation_steps'] = 'not_an_int'
    with pytest.raises(ValueError, match="validation_steps must be an integer"):
        trainer_validator.validate_validation_steps()

def test_validate_video_column_invalid(trainer_validator):
    trainer_validator.config['video_column'] = 123
    with pytest.raises(ValueError, match="video_column must be a string"):
        trainer_validator.validate_video_column()

def test_validate_video_resolution_buckets_invalid(trainer_validator):
    trainer_validator.config['video_resolution_buckets'] = 123
    with pytest.raises(ValueError, match="video_resolution_buckets must be a string"):
        trainer_validator.validate_video_resolution_buckets()
    trainer_validator.config['video_resolution_buckets'] = '720p,1080p,4k'
    with pytest.raises(ValueError, match=f"Each bucket must have the format '<frames>x<height>x<width>', but got {trainer_validator.config['video_resolution_buckets']}"):
        trainer_validator.validate_video_resolution_buckets()

def test_validate_video_resolution_buckets_valid(trainer_validator):
    trainer_validator.config['video_resolution_buckets'] = '24x480x720'
    trainer_validator.validate_video_resolution_buckets()

    trainer_validator.config['video_resolution_buckets'] = '8x320x512 24x480x720 30x720x1280'
    trainer_validator.validate_video_resolution_buckets()

def test_validate_weight_decay_invalid(trainer_validator):
    trainer_validator.config['weight_decay'] = 'not_a_float'
    with pytest.raises(ValueError, match="weight_decay must be a float"):
        trainer_validator.validate_weight_decay()