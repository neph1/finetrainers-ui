
import gradio as gr
from typing import OrderedDict

from tabs.tab import Tab

properties = OrderedDict()

class GeneralTab(Tab):

    def __init__(self, title, config_file_path, allow_load=False):
        super().__init__(title, config_file_path, allow_load)
    
        try:
            with self.config_inputs:
                self.components = OrderedDict(self.update_form(self.config))
                for i in range(len(self.config_inputs.children)):
                    keys = list(self.components.keys())
                    properties[keys[i]] = self.config_inputs.children[i]

        except Exception as e:
            gr.Error(f"Error loading config file: {e}")
            
        with gr.Row(equal_height=False):
            self.add_buttons()

    def get_properties(self) -> OrderedDict:
        return properties