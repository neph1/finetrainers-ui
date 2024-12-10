from typing import OrderedDict
import gradio as gr
import yaml
import editor_factory

properties = OrderedDict()
class Tab:

    
    def __init__(self, title, config_file_path, allow_load=False):
        self.title = title
        self.allow_load = allow_load
        gr.Markdown(title)
    
        self.status = gr.Markdown()
        self.config_inputs = gr.Column("Settings")
        self.save_status = gr.Markdown()
        try:
            self.config = self.load_config(config_file_path)
            with self.config_inputs:
                self.components = OrderedDict(self.update_form(self.config))
                for i in range(len(self.config_inputs.children)):
                    keys = list(self.components.keys())
                    properties[keys[i]] = self.config_inputs.children[i]
        except Exception as e:
            gr.Error(f"Error loading config file: {e}")
        self.config_file_box = gr.Textbox(value=config_file_path, label="Config file")
        with gr.Row(equal_height=False):
            self.add_buttons()


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
        keys_list = list(properties.keys())

        try:
            for key in keys_list:
                if key not in self.config.keys():
                    continue
                index = keys_list.index(key)
                value = properties_values[index]
                self.config[key] = value if value else False
            self.save_config(config_file)
            return f"Config saved successfully: {self.config} to {config_file}", config_file
        except Exception as e:
            return f"Error saving config: {e}", ""

    def add_buttons(self):
        """Add Save and Load buttons for the tab."""
        if self.allow_load:
            config_file = gr.File(label="Upload Config File")
        save_button = gr.Button("Save Config")

        save_button.click(
            self.save_edits,
            inputs=[self.config_file_box, *properties.values()],
            outputs=[self.save_status, self.config_file_box]
        )

        if self.allow_load:
            load_button = gr.Button("Load Config")
            load_button.click(
                render_editor, 
                inputs=[config_file, self.config_file_box, *properties.values()], 
                outputs=[self.save_status, self.config_file_box, *properties.values()]
            )

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
                inputs[key] = (gr.Textbox(value=value, label=key))
            elif isinstance(value, list):
                inputs[key] = (gr.Dropdown(value=value[0], label=key, choices=value))
            else:
                inputs[key] = (gr.Textbox(value=str(value), label=key))  # Default to text for unsupported types
            
        return inputs
    
def render_editor(*args):
    args_list = list(args)
    config_file = args_list[0]
    config_file_box = args_list[1]
    properties_values = args_list[2:]
    try:
        with open(config_file, "r") as file:
            new_config = yaml.safe_load(file)
            
        props_list = list(properties.keys())
        for key, value in new_config.items():
            index = props_list.index(key)
            properties_values[index] = value
            properties[key].value = value
        return ["Config loaded. Edit below:", config_file_box, *properties_values]
    except Exception as e:
        return [f"Error loading config: {e}", config_file_box, *properties_values]