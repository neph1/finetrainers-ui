import os
import pytest
from unittest.mock import patch

from trainer_config_validator import TrainerValidator

@pytest.fixture
def valid_config():
    return {
        'path_to_finetrainers': '/path/to/finetrainers',
        'accelerate_config': 'config1',
        'batch_size': 32,
        'beta1': 0.9,
        'beta2': 0.999,
        'caption_column': 'captions.txt',
        'caption_dropout_p': 0.1,
        'checkpointing_limit': 5,
        'checkpointing_steps': 1000,
        'data_root': '/path/to/data',
        'dataloader_num_workers': 0,
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
        'rank': 64,
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

def test_validate_data_root_invalid(trainer_validator):
    trainer_validator.config['data_root'] = '/invalid/path'
    with pytest.raises(ValueError, match="data_root path /invalid/path does not exist"):
        trainer_validator.validate_data_root()

def test_validate_data_root_valid(trainer_validator):
    with patch('os.path.exists', return_value=True), patch('os.path.isdir', return_value=True):
        trainer_validator.config['data_root'] = '/path/to/data'
        trainer_validator.validate_data_root()

def test_validate_video_resolution_buckets_invalid(trainer_validator):
    trainer_validator.config['video_resolution_buckets'] = '720p,1080p,4k'
    with pytest.raises(ValueError, match=f"Each bucket must have the format '<frames>x<height>x<width>', but got {trainer_validator.config['video_resolution_buckets']}"):
        trainer_validator.validate_video_resolution_buckets()

def test_validate_video_resolution_buckets_valid(trainer_validator):
    trainer_validator.config['video_resolution_buckets'] = '24x480x720'
    trainer_validator.validate_video_resolution_buckets()

    trainer_validator.config['video_resolution_buckets'] = '8x320x512 24x480x720 30x720x1280'
    trainer_validator.validate_video_resolution_buckets()
