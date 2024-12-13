import os
import time
import shutil
import tkinter as tk
import json

def create_backup(window, game, yuzu_saves, ryujinx_saves, backup_saves):

    def create_overlay(title, message, confirm_callback=None, cancel_callback=None, show_backup_entry=False):
        scale_factor = window.winfo_height() / 800

        blocker = tk.Frame(window, bg="#333333")
        blocker.place(relx=0, rely=0, relwidth=1, relheight=1)

        overlay_frame = tk.Frame(window, bg="#333333", width=int(300 * scale_factor), height=int(300 * scale_factor) if show_backup_entry else int(200 * scale_factor))
        overlay_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(overlay_frame, text=title, font=("Arial", int(14 * scale_factor), "bold"), fg="#FFFFFF", bg="#333333")
        title_label.pack(pady=(int(10 * scale_factor), int(5 * scale_factor)))

        message_label = tk.Label(overlay_frame, text=message, font=("Arial", int(12 * scale_factor)), fg="#FFFFFF", bg="#333333", wraplength=int(280 * scale_factor))
        message_label.pack(pady=(int(5 * scale_factor), int(10 * scale_factor)))

        emulator_display = game.get('emulator', 'Emulator')
        backup_name_var = tk.StringVar(value=f"{emulator_display} - {time.strftime('%Y.%m.%d @ %H.%M.%S')}")

        if show_backup_entry:
            backup_name_entry = tk.Entry(overlay_frame, textvariable=backup_name_var, font=("Arial", int(12 * scale_factor)), width=int(30 * scale_factor))
            backup_name_entry.pack(pady=(int(5 * scale_factor), int(10 * scale_factor)))

        button_frame = tk.Frame(overlay_frame, bg="#333333")
        button_frame.pack(pady=(int(5 * scale_factor), int(10 * scale_factor)))

        def close_overlay():
            blocker.destroy()
            overlay_frame.destroy()

        def confirm_and_backup():
            backup_name = backup_name_var.get().strip() if show_backup_entry else None
            close_overlay()
            if confirm_callback:
                confirm_callback(backup_name)

        if confirm_callback:
            yes_button = tk.Button(
                button_frame,
                text="Yes",
                relief="flat",
                command=confirm_and_backup,
                bg="#19D719",
                fg="#FFFFFF",
                font=("Arial", int(10 * scale_factor), "bold"),
                width=int(12 * scale_factor)
            )
            yes_button.pack(side=tk.LEFT, padx=int(10 * scale_factor))

            no_button = tk.Button(
                button_frame,
                text="No",
                relief="flat",
                command=close_overlay,
                bg="#F02D7D",
                fg="#FFFFFF",
                font=("Arial", int(10 * scale_factor), "bold"),
                width=int(12 * scale_factor)
            )
            no_button.pack(side=tk.LEFT, padx=int(10 * scale_factor))
        else:
            ok_button = tk.Button(
                button_frame,
                text="OK",
                relief="flat",
                command=close_overlay,
                bg="#19D719",
                fg="#FFFFFF",
                font=("Arial", int(10 * scale_factor), "bold"),
                width=int(12 * scale_factor)
            )
            ok_button.pack(side=tk.LEFT, padx=int(10 * scale_factor))

            if cancel_callback:
                cancel_button = tk.Button(
                    button_frame,
                    text="Cancel",
                    relief="flat",
                    command=lambda: [cancel_callback(), close_overlay()],
                    bg="#F02D7D",
                    fg="#FFFFFF",
                    font=("Arial", int(10 * scale_factor), "bold"),
                    width=int(12 * scale_factor)
                )
                cancel_button.pack(side=tk.LEFT, padx=int(10 * scale_factor))

    try:
        with open('data/config.json', 'r') as f:
            config = json.load(f)
            auto_backup_name = config.get('auto_backup_name', False)
            backups_zip = config.get('backups_zip', True)
    except Exception as e:
        create_overlay("Error", f"Error loading config: {e}")
        return

    def confirm_backup(zip_name):
        game_id = game["id"]
        game_name = zip_name if zip_name else game.get("emulator")

        if game["emulator"] == "Yuzu":
            save_path = os.path.join(yuzu_saves, game_id)
        elif game["emulator"] == "Ryujinx":
            save_path = os.path.join(ryujinx_saves, game_id, '0')

        if not os.path.exists(save_path):
            create_overlay("Error", f"Save folder not found for game '{game['name']}'")
            return

        if not any(os.path.isfile(os.path.join(save_path, f)) for f in os.listdir(save_path)):
            create_overlay("Error", f"No saved files found for game '{game['name']}'")
            return

        timestamp = time.strftime("%Y.%m.%d @ %H.%M.%S")
        zip_name = zip_name.replace(".zip", "")
        folder_name = game["name"]
        folder_path = os.path.join(backup_saves, folder_name, zip_name)

        if os.path.exists(folder_path):
            create_overlay(
                "File Exists",
                f"The backup folder '{folder_name}' already exists. Do you want to overwrite it?",
                confirm_callback=lambda _: perform_backup(save_path, folder_path, backups_zip),
                cancel_callback=lambda: create_backup(window, game, yuzu_saves, ryujinx_saves, backup_saves)
            )
        else:
            perform_backup(save_path, folder_path, backups_zip)

    def perform_backup(save_path, folder_path, backups_zip):
        if backups_zip:
            zip_path = folder_path + ".zip"
            shutil.make_archive(zip_path.replace(".zip", ""), 'zip', save_path)
            create_overlay("Success", f"Backup completed successfully for game '{game['name']}' as ZIP file.")
        else:
            os.makedirs(folder_path, exist_ok=True)
            for item in os.listdir(save_path):
                s = os.path.join(save_path, item)
                d = os.path.join(folder_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            create_overlay("Success", f"Backup completed successfully for game '{game['name']}' in folder '{folder_path}'.")

    if auto_backup_name:
        game_name = game.get("emulator")
        timestamp = time.strftime("%Y.%m.%d @ %H.%M.%S")
        zip_name = f"{game_name} - {timestamp}"
        create_overlay("Confirm", f"Do you want to backup the game '{game['name']}' with the name '{zip_name}'?", confirm_callback=lambda _: confirm_backup(zip_name))
        return

    def submit_custom_name(name):
        zip_name = name
        create_overlay("Confirm", f"Do you want to backup the game '{game['name']}' with the name '{zip_name}'?", confirm_callback=lambda _: confirm_backup(zip_name))

    create_overlay("Enter Backup Name", "Please enter a name for the backup.", confirm_callback=submit_custom_name, show_backup_entry=True)
