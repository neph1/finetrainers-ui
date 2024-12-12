
import gradio as gr
from typing import OrderedDict

import yaml
from tabs.tab import Tab

properties = OrderedDict()

class GeneralTab(Tab):

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

    def get_properties(self) -> OrderedDict:
        return properties
    
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
            #properties[key].value = value
        return ["Config loaded. Edit below:", config_file_box, *properties_values]
    except Exception as e:
        return [f"Error loading config: {e}", config_file_box, *properties_values]