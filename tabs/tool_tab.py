import gradio as gr

from scripts import rename_keys

class ToolTab:

    def __init__(self):
        gr.Markdown("Lora Tools")
        self._build_rename()

    def _build_rename(self):
        gr.Markdown("Rename Transformer Keys")
        rename_in_file = gr.Textbox(value="", label="Lora to rename (full path)", lines=1)
        rename_out_file = gr.Textbox(value="", label="New name (full path)", lines=1)
        rename_result = gr.Textbox(value="", label="Result", lines=1)
        rename_button = gr.Button("Rename", key='rename')
        rename_button.click(self.rename_file, inputs=[rename_in_file, rename_out_file], outputs=[rename_result])

    def rename_file(self, lora_name, new_name):
        result = rename_keys.rename_keys(lora_name, new_name)
        if result:
            return "Renamed successfully"