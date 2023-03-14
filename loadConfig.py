import json
import os


def load_config():
    try:
        with open(os.path.join("__config", "app_config.json")) as app_config_file:
            data = json.load(app_config_file)
            app_config_file.close()
            return data
    except (Exception) as e:
        return []
