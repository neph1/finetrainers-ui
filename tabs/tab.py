from abc import ABC
from typing import OrderedDict
import gradio as gr
import yaml
import editor_factory

class Tab(ABC):

    def __init__(self, title, config_file_path, allow_load=False):
        pass

    def load_config(self, file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def save_config(self, file_path):
        with open(file_path, "w") as file:
            yaml.dump(self.config, file, default_flow_style=False)

    def save_edits(self,*args):
        args_list = list(args)
        config_file = args_list[0]
        properties_values = args_list[1:]
        properties = self.get_properties()
        keys_list = list(properties.keys())
        print("1")

        try:
            for key in keys_list:
                if key not in self.config.keys():
                    continue
                index = keys_list.index(key)
                value = properties_values[index]
                print("2")
                self.config[key] = value if value else False
            self.save_config(config_file)
            print("3")
            return f"Config saved successfully: {self.config} to {config_file}", config_file
        except Exception as e:
            return f"Error saving config: {e}", ""

    def add_buttons(self):
        """Add Save and Load buttons for the tab."""
        pass

    def update_form(self, config):
        inputs = dict()
        for key, value in config.items():
            value = value or editor_factory.get_default_value_for_key(key)
            if isinstance(value, bool):
                inputs[key] = (gr.Checkbox(value=value, label=key))
            elif isinstance(value, int):
                inputs[key] = (gr.Number(value=value, label=key, precision=0))
            elif isinstance(value, float):
                inputs[key] = (gr.Number(value=value, label=key))
            elif isinstance(value, str):
                inputs[key] = (gr.Textbox(value=value, label=key, interactive=True))
            elif isinstance(value, list):
                inputs[key] = (gr.Dropdown(value=value[0], label=key, choices=value))
            else:
                inputs[key] = (gr.Textbox(value=str(value), label=key))  # Default to text for unsupported types
            
        return inputs
    
    def get_properties(self) -> OrderedDict:
        pass
    
    def render_editor(self, *args):
        pass