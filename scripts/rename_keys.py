import argparse
import torch

from scripts.common_io import load_state_dict, save_to_file


def rename_keys(file, outfile: str)-> bool:
    sd, metadata = load_state_dict(file, torch.float32)

    keys_to_normalize = [key for key in sd.keys()]
    values_to_normalize = [sd[key].to(torch.float32) for key in keys_to_normalize]
    new_sd = dict()
    for key, value in zip(keys_to_normalize, values_to_normalize):
        new_sd[key.replace("transformer.", "")] = value
        
    save_to_file(outfile, new_sd, torch.float16, metadata)
    return True

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="lora model to modify")
    parser.add_argument("-o", "--outfile", type=str, help="file to save to")
    return parser


if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()
    rename_keys(args.file, args.outfile)
