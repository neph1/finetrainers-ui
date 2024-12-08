import os
import gradio as gr

from config import global_config
from runner import RunCogVideoX
from tab import Tab, properties


class App:

    def __init__(self):
        self.configs_path = "config/"
        self.general_config_path = os.path.join(self.configs_path, "editor.yaml")
        self.runtime_config_path = os.path.join(self.configs_path, "config_template.yaml")
        self.tabs = dict() # Type Tab
        self.setup_views()

    def setup_views(self):
        with gr.Blocks() as demo:
            gr.Markdown("### cogvideox-factory config editor")

            with gr.Tab("General Settings"):
                self.tabs['general'] = Tab("General Settings", self.general_config_path)
            
            with gr.Tab("Runtime Settings"):
                self.tabs['runtime'] = Tab("Runtime Settings", self.runtime_config_path, allow_load=True)

            run_button = gr.Button("Run", key='run_cogvideox')
            run_button.click(run_cogvideox, 
                            inputs=[*properties.values()],
                            outputs=[]
                            )
        demo.launch()

def run_cogvideox(*args):
    properties_values = list(args)
    keys_list = list(properties.keys())
    for index in range(len(properties_values)):
        key = keys_list[index]
        properties[key].value = properties_values[index]
        global_config.set(key, properties_values[index])
    output_path = os.path.join(global_config.get('output_dir'), "config")
    os.makedirs(output_path, exist_ok=True)
    #self.tabs['runtime'].save_config(os.path.join(output_path, "runtime_config.yaml"))
    RunCogVideoX()

if __name__ == "__main__":
    App()