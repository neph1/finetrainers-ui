import streamlit as st
import yaml

class Tab:

    def __init__(self, title, config_file_path, allow_load = False):
        self.title = title
        try:
            self.config_data = self.load_config(config_file_path)
        except Exception as e:
            st.error(f"Error loading config file: {e}")
            st.stop()
        self.in_memory_data = {}
        self.update_view()
        self.add_buttons(config_file_path, allow_load)

    def load_config(self, file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def save_config(self, file_path):
        with open(file_path, "w") as file:
            yaml.dump(self.in_memory_data, file, default_flow_style=False)


    def add_buttons(self, config_file_path, allow_load):
        
        # Save button
        if st.button("Save Config", key=config_file_path):
            try:
                self.save_config(config_file_path)
                st.success("Config file saved successfully!")
            except Exception as e:
                st.error(f"Error saving config file: {e}")

        if allow_load:
            uploaded_file = st.file_uploader("Load Config", type=["yaml", "yml"])
            if uploaded_file is not None:
                try:
                    # Read the uploaded file
                    self.config_data = yaml.safe_load(uploaded_file)
                    self.update_view()
                    # Optionally overwrite the existing config in the editor
                    st.success("Config file loaded")
                except Exception as e:
                    st.error(f"Error loading config file: {e}")

    
    def update_view(self):
        self.in_memory_data = {}
        for key, value in self.config_data.items():
            if isinstance(value, bool):
                self.in_memory_data[key] = st.checkbox(key, value=value)
            elif isinstance(value, int):
                self.in_memory_data[key] = st.number_input(key, value=value)
            elif isinstance(value, float):
                self.in_memory_data[key] = st.number_input(key, value=value, format="%.2f")
            elif isinstance(value, list):
                self.in_memory_data[key] = st.selectbox(
    key,
    value,
)
            else:
                self.in_memory_data[key] = st.text_input(key, value=value)
            
