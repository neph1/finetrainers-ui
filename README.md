# cogvideox-factory-ui


Simple GUI for [cogvideox-factory](https://github.com/a-r-r-o-w/cogvideox-factory) (but in no way affiliated with it) made using gradio, inspired by bmalthais gui for kohya-ss scripts.

Doesn't contain cogvideox-factory. You must download it and get it running separately.

Load and save configurations

Finetuning and Prepare dataset tabs



Usage:

Have CogvideoX-Factory

Clone repo

Install streamlit `pip install gradio`

Run with `python app.py`

Config path to cogvideox-factory in app

Configure your runtime settings

Press run

Cross fingers and hope it works



Early days: May not work as expected.

The editor is pretty dumb at the moment, and formatting is expected to be the same as in the .sh files, ie spaces between buckets, comma between gpu_ids.


Tip:
If I've missed any configuration options you want, you can add them to `configs/config_template.yaml` and they will be picked up by the app.
