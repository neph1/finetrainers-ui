import os

import gradio as gr

from config import global_config
from tabs.general_tab import GeneralTab
from tabs.prepare_tab import PrepareDatasetTab
from tabs.tab import Tab
from tabs.training_tab import TrainingTab
from tabs.training_tab_legacy import LegacyTrainingTab


class App:


    runtime_tab = None
    prepare_tab = None

    def __init__(self):
        self.configs_path = "config/"
        self.tabs = dict() # Type Tab
        self.setup_views()

    def setup_views(self):
        with gr.Blocks() as demo:
            gr.Markdown("### cogvideox-factory config editor")


            with gr.Tab("General Settings"):
                self.tabs['general'] = GeneralTab("General Settings", os.path.join(self.configs_path, "editor.yaml"))
            runtime_tab = gr.Tab("Trainer Settings")
            prepare_tab = gr.Tab("Prepare dataset")
            runtime_tab_legacy = gr.Tab("Legacy Training Settings")

            with runtime_tab:
                self.tabs['runtime'] = TrainingTab("Trainer Settings", os.path.join(self.configs_path, "config_template.yaml"), allow_load=True)

            
            with prepare_tab:
                self.tabs['prepare'] = PrepareDatasetTab("Prepare dataset", os.path.join(self.configs_path, "prepare_template.yaml"), allow_load=True)
            
            with runtime_tab_legacy:
                self.tabs['runtime'] = LegacyTrainingTab("Legacy CogvideoX Settings", os.path.join(self.configs_path, "config_template_legacy.yaml"), allow_load=True)

            
        demo.launch()


if __name__ == "__main__":
    App()