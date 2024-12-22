import gradio as gr


def get_editor_for_key(key, value):
    """Return the appropriate editor for the given key and value."""
    if isinstance(value, list):
        return gr.Dropdown(label=key, choices=value)
    if isinstance(value, bool):
        return gr.Checkbox(label=key, default=value)
    if isinstance(value, int):
        return gr.Number(label=key, default=value)
    if isinstance(value, float):
        return gr.Number(label=key, default=value)
    if isinstance(value, str):
        return gr.Textbox(label=key, default=value)
    if isinstance(value, list):
        return gr.Textbox(label=key, default=str(value))
    if isinstance(value, dict):
        return gr.Textbox(label=key, default=str(value))
    return gr.Textbox(label=key, default=str(value))
