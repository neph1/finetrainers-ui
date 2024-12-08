import gradio as gr


def get_editor_for_key(key, value):
    """Return the appropriate editor for the given key and value."""
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

def get_default_value_for_key(key):
    """Return the default value for the given key."""
    if key == "path_to_cogvideox_factory":
        return "/path/to/cogvideox-factory"
    if key == "training_type":
        return ["cogvideox_text_to_video_sft", "cogvideox_image_to_video_lora", "cogvideox_text_to_video_lora"]
    if key == "mixed_precision":
        return ["fp16", "bf16", "no"]
    if key == "optimizer":
        return ["adam", "adamw"]
    return None