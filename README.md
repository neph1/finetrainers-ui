# finetrainers-ui


Simple GUI for [finetrainers](https://github.com/a-r-r-o-w/finetrainers) (but in no way affiliated with it) made using gradio, inspired by bmalthais gui for kohya-ss scripts.

The goal is to be able to reproduce and analyze previous runs by saving meta data. 

Doesn't contain cogvideox-factory. You must download it and get it running separately.

I try to keep main stable, but if it fails, step back one version and try that.


![Screenshot from 2024-12-30 07-56-37](https://github.com/user-attachments/assets/91b947db-1e50-42e0-8d12-28b436bf837d)

v0.7.0: Added a new tab for "Lora tools" and a rename script that changes the keys of loras to allow them to be loaded in (some versions of?) ComfyUI

v0.6.0: Collapsible categories for settings

v0.4.0: Saving log to output folder

v0.3.0: Saving config file to output folder

Tabs for training and prepare dataset (legacy)

I'm migrating to the new finetrainers structure. Currently tested with LTX-Video. Keeping legacy CogVideoX trainer in the "Legacy" tab.




Usage:

Have ~~CogvideoX-Factory~~ finetrainers

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
