import os
import streamlit as st

from runner import RunCogVideoX
from tab import Tab


class App:

    def __init__(self):

        self.configs_path = "config/"
        self.general_config_path = os.path.join(self.configs_path, "editor.yaml")
        self.runtime_config_path = os.path.join(self.configs_path, "config_template.yaml")
        self.tabs = dict()
        self.setup_views()

    def setup_views(self):
        st.title("Multi-Config File Editor")
        tabs = st.tabs(["General Settings", "Runtime Settings"])

        with tabs[0]:
            st.subheader("General Settings")
            self.tabs['general'] = Tab("General Settings", self.general_config_path)

        with tabs[1]:
            st.subheader("Runtime Settings")
            self.tabs['runtime'] = Tab("Runtime Settings", self.runtime_config_path, allow_load=True)

        if st.button("Run", key='run_cogvideox'):

            settings = self.tabs['runtime'].in_memory_data
            output_path = os.path.join(settings['output_dir'], "config")
            os.makedirs(output_path, exist_ok=True)
            self.tabs['runtime'].save_config(os.path.join(output_path, "runtime_config.yaml"))
            RunCogVideoX(self.tabs['general'].in_memory_data['path_to_cogvideox_factory'], settings)


if __name__ == "__main__":
    App()