import json
from tkinter import filedialog, messagebox

from app.config.config_manager import load_log, save_log, CONFIG_FILE

def configure_backup_folder():
    folder_path = filedialog.askdirectory(title="Select Backup Folder")
    if folder_path:
        config_data = load_log()
        config_data['saves_backups'] = folder_path

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)

        return True
    return False

def configure_yuzu_folder():
    config_data = load_log()
    if not config_data.get('saves_backups'):
        messagebox.showwarning("Error", "Please configure a backup folder first.")
        if not configure_backup_folder():
            return False
        config_data = load_log()

    folder_path = filedialog.askdirectory(title="Select Yuzu Folder")
    if folder_path:
        config_data['saves_yuzu'] = folder_path
        save_log(
            config_data['saves_yuzu'],
            config_data['saves_ryujinx'],
            config_data['saves_backups'],
            config_data['auto_backups_on'],
            config_data['auto_backup_name'],
            config_data['backups_zip']
        )
        return True
    return False

def configure_ryujinx_folder():
    config_data = load_log()
    if not config_data.get('saves_backups'):
        messagebox.showwarning("Error", "Please configure a backup folder first.")
        if not configure_backup_folder():
            return False
        config_data = load_log()

    folder_path = filedialog.askdirectory(title="Select Ryujinx Folder")
    if folder_path:
        config_data['saves_ryujinx'] = folder_path
        save_log(
            config_data['saves_yuzu'],
            config_data['saves_ryujinx'],
            config_data['saves_backups'],
            config_data['auto_backups_on'],
            config_data['auto_backup_name'],
            config_data['backups_zip']
        )
        return True
    return False
