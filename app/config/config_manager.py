import json
import os

CONFIG_FILE = os.path.join("data", "config.json")

def load_log():
    if not os.path.exists(CONFIG_FILE):
        return {
            "saves_yuzu": "",
            "saves_ryujinx": "",
            "saves_backups": ""
        }

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config_data = json.load(file)
        return config_data
    except (json.JSONDecodeError, KeyError):
        return {
            "saves_yuzu": "",
            "saves_ryujinx": "",
            "saves_backups": ""
        }

def save_log(saves_yuzu, saves_ryujinx, saves_backups, auto_backups_on, auto_backup_name, backups_zip):
    data = {
        "saves_yuzu": saves_yuzu,
        "saves_ryujinx": saves_ryujinx,
        "saves_backups": saves_backups,
        "auto_backups_on": auto_backups_on,
        "auto_backup_name": auto_backup_name,
        "backups_zip": backups_zip
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def ensure_configurations():
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(CONFIG_FILE):
        save_log("", "", "", True, False, False)

ensure_configurations()
