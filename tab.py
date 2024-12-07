import streamlit as st
import yaml

class Tab:
    def __init__(self, title, config_file_path, allow_load=False):
        self.title = title
        self.config_file_path = config_file_path
        self.session_key = f"config_{title}" 
        self.allow_load = allow_load

        if self.session_key not in st.session_state:
            try:
                st.session_state[self.session_key] = self.load_config(config_file_path)
            except Exception as e:
                st.error(f"Error loading config file: {e}")
                st.stop()

        # Display the UI
        self.update_view()
        self.add_buttons()

    def load_config(self, file_path):
        """Load a YAML configuration file."""
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def save_config(self, file_path):
        """Save the current configuration to a YAML file."""
        with open(file_path, "w") as file:
            yaml.dump(st.session_state[self.session_key], file, default_flow_style=False)

    def add_buttons(self):
        """Add Save and Load buttons for the tab."""
        if st.button(f"Save Config ({self.title})", key=f"save_{self.title}"):
            try:
                self.save_config(self.config_file_path)
                st.success(f"Config for {self.title} saved successfully!")
            except Exception as e:
                st.error(f"Error saving config file: {e}")

        if self.allow_load:
            uploaded_file = st.file_uploader(f"Load Config for {self.title}", type=["yaml", "yml"])
            if uploaded_file is not None:
                try:
                    loaded_data = yaml.safe_load(uploaded_file)
                    st.session_state[self.session_key] = loaded_data
                    st.success(f"Config for {self.title} loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading config file: {e}")

    def update_view(self):
        """Update the form fields based on the current configuration."""
        config_data = st.session_state[self.session_key]
        updated_config = {}
        for key, value in config_data.items():
            if isinstance(value, bool):
                updated_config[key] = st.checkbox(key, value=value, key=f"{self.title}_{key}")
            elif isinstance(value, int):
                updated_config[key] = st.number_input(key, value=value, key=f"{self.title}_{key}")
            elif isinstance(value, float):
                updated_config[key] = st.number_input(key, value=value, format="%.2f", key=f"{self.title}_{key}")
            elif isinstance(value, list):
                updated_config[key] = st.selectbox(key, value, key=f"{self.title}_{key}")
            else:
                updated_config[key] = st.text_input(key, value=value, key=f"{self.title}_{key}")
        st.session_state[self.session_key] = updated_config