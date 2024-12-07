from typing import OrderedDict
import gradio as gr
import yaml

properties = OrderedDict()
class Tab:
    def __init__(self, title, config_file_path, allow_load=False):
        self.title = title
        self.config_file_path = config_file_path
        self.session_key = f"config_{title}" 
        self.allow_load = allow_load
        gr.Markdown("### YAML Config Editor")
    
        self.status = gr.Markdown()
        self.config_inputs = gr.Column("Settings")
        self.save_status = gr.Markdown()
        try:
            config = self.load_config(config_file_path)
            with self.config_inputs:
                self.components = OrderedDict(self.update_form(config))
                for i in range(len(self.config_inputs.children)):
                    keys = list(self.components.keys())
                    properties[keys[i]]=self.config_inputs.children[i]
        except Exception as e:
            gr.error(f"Error loading config file: {e}")

        self.add_buttons()

    def load_config(self, file_path):
        """Load a YAML configuration file."""
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def save_config(self, file_path):
        """Save the current configuration to a YAML file."""
        with open(file_path, "w") as file:
            yaml.dump(self.get_config(), file, default_flow_style=False)

    def save_edits(self, config_file, *inputs):
        try:
            config = yaml.safe_load(config_file)
            updated_config = {key: value for key, value in zip(config.keys(), inputs)}
            self.save_config("updated_config.yaml", updated_config)
            return f"Config saved successfully: {updated_config}"
        except Exception as e:
            return f"Error saving config: {e}"

    def add_buttons(self):
        """Add Save and Load buttons for the tab."""
        config_file = gr.File(label="Upload Config File")
        save_button = gr.Button("Save Config")
        save_button.click(
            self.save_edits,
            inputs=[config_file],
            outputs=[self.save_status]
        )

        if self.allow_load:
            
            load_button = gr.Button("Load Config")
            load_button.click(
                render_editor, 
                inputs=[config_file, *properties.values()], 
                outputs=[self.save_status, *properties.values()]
            )

    def update_values(self, config):
        for key, value in config.items():
            self.properties[key] = value

    def update_form(self, config):
        inputs = dict()
        for key, value in config.items():
            if isinstance(value, bool):
                inputs[key] = (gr.Checkbox(value=value, label=key))
            elif isinstance(value, int):
                inputs[key] = (gr.Number(value=value, label=key, precision=0))
            elif isinstance(value, float):
                inputs[key] = (gr.Number(value=value, label=key))
            elif isinstance(value, str):
                inputs[key] = (gr.Textbox(value=value, label=key))
            else:
                inputs[key] = (gr.Textbox(value=str(value), label=key))  # Default to text for unsupported types
        return inputs

def get_config()-> dict:
    config = dict()
    for key, value in properties.items():
        config[key] = value.value
    return config

def render_editor(*args):
    inputs = list(args)
    try:
        with open(inputs[0], "r") as file:
            config = yaml.safe_load(file)
        props_list = list(properties.keys())
        for key, value in config.items():
            index = props_list.index(key) + 1
            inputs[index] = value
        return ["Config loaded. Edit below:", *inputs[1:]]
    except Exception as e:
        return [f"Error loading config: {e}", *inputs[1:]]