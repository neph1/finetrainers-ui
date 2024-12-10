import os
import gradio as gr

from config import global_config
from runner import RunCogVideoX, RunPrepareDataset
from tab import Tab, properties


class App:


    runtime_tab = None
    prepare_tab = None

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
                self.tabs['general'] = Tab("General Settings", os.path.join(self.configs_path, "editor.yaml"))
            runtime_tab = gr.Tab("Runtime Settings")
            prepare_tab = gr.Tab("Prepare dataset")
            output_box = gr.Textbox(value="", label="Output")
            
            with runtime_tab:
                self.tabs['runtime'] = Tab("Runtime Settings", os.path.join(self.configs_path, "config_template.yaml"), allow_load=True)
                run_button = gr.Button("Run Training", key='run_cogvideox')
                run_button.click(run_cogvideox, 
                                inputs=[*properties.values()],
                                outputs=[output_box]
                                )

            with prepare_tab:
                self.tabs['prepare'] = Tab("Prepare dataset", os.path.join(self.configs_path, "prepare_template.yaml"), allow_load=True)
                run_button = gr.Button("Prepare dataset", key='prepare_dataset')
                run_button.click(run_prepare_data, 
                                inputs=[*properties.values()],
                                outputs=[output_box]
                                )
            
        demo.launch()

def run_cogvideox(*args):
    properties_values = list(args)
    keys_list = list(properties.keys())
    for index in range(len(properties_values)):
        key = keys_list[index]
        properties[key].value = properties_values[index]
        global_config.set(key, properties_values[index])
    output_path = os.path.join(global_config.get('output_dir', 'train'), "config")
    os.makedirs(output_path, exist_ok=True)
    #self.tabs['runtime'].save_config(os.path.join(output_path, "runtime_config.yaml"))
    result = RunCogVideoX().run_cogvideox(global_config)
    if result.returncode == 0:
        return "Run Training: Training completed successfully"
    else:
        return "Run Training: Training failed"

def run_prepare_data(*args):
    properties_values = list(args)
    keys_list = list(properties.keys())
    for index in range(len(properties_values)):
        key = keys_list[index]
        value = properties_values[index]
        properties[key].value = value
        global_config.set(key, value)
        print("path",key, value)
    output_path = os.path.join(global_config.get('output_dir', 'prepare'), "config")
    os.makedirs(output_path, exist_ok=True)
    #self.tabs['runtime'].save_config(os.path.join(output_path, "runtime_config.yaml"))
    result = RunPrepareDataset().run(global_config)
    if result.returncode == 0:
        return "Prepate dataset: Dataset prepared successfully"
    else:
        return "Prepate dataset: Dataset preparation failed"

if __name__ == "__main__":
    App()