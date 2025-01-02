import os
import torch
from safetensors.torch import load_file, save_file, safe_open

def load_state_dict(file_name, dtype):
    if os.path.splitext(file_name)[1] == ".safetensors":
        sd = load_file(file_name)
        with safe_open(file_name, framework="pt") as f:
            metadata = f.metadata()
    else:
        sd = torch.load(file_name, map_location="cpu")
        metadata = None

    for key in list(sd.keys()):
        if type(sd[key]) == torch.Tensor:
            sd[key] = sd[key].to(dtype)

    return sd, metadata

def save_to_file(file_name, state_dict, dtype, metadata):
    if dtype is not None:
        for key in list(state_dict.keys()):
            if type(state_dict[key]) == torch.Tensor:
                state_dict[key] = state_dict[key].to(dtype) 
    if os.path.splitext(file_name)[1] == ".safetensors":
        save_file(state_dict, file_name, metadata)
    else:
        torch.save(state_dict, file_name)
