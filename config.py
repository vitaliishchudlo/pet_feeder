import json
import constants

CONFIG_FILE_NAME = None # like config.json

def set_config_file_name(config_file_name):
    global CONFIG_FILE_NAME
    CONFIG_FILE_NAME = config_file_name
    

def create_config_file():
    try:
        with open(CONFIG_FILE_NAME, 'w') as file:
            file.write(json.dumps(constants.DATABASE_BODY))
        return True
    except Exception:
        raise

def read_config():
    try:
        with open(CONFIG_FILE_NAME, 'r') as file:
            config_file = file.read()
            config_json = json.loads(config_file)
        return config_json
    except Exception:
        raise

def change_config(new_config: dict):
    if not isinstance(new_config, dict):
        return False    
    try:
        with open(CONFIG_FILE_NAME, 'w') as file:
            file.write(json.dumps(new_config))
        return new_config
    except Exception:
        raise