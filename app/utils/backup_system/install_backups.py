import os
import json
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import shutil
import zipfile

def install_backup(window, game, yuzu_saves, ryujinx_saves):

    def create_overlay(title, message, show_options=False, show_confirmation=False, on_confirm=None):
        scale_factor = window.winfo_height() / 800

        blocker = tk.Frame(window, bg="#333333")
        blocker.place(relx=0, rely=0, relwidth=1, relheight=1)

        overlay_frame = tk.Frame(window, bg="#333333", width=int(300 * scale_factor), height=int(200 * scale_factor) if not show_options else int(300 * scale_factor))
        overlay_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(overlay_frame, text=title, font=("Arial", int(14 * scale_factor), "bold"), fg="#FFFFFF", bg="#333333")
        title_label.pack(pady=(int(10 * scale_factor), int(5 * scale_factor)))

        message_label = tk.Label(overlay_frame, text=message, font=("Arial", int(12 * scale_factor)), fg="#FFFFFF", bg="#333333", wraplength=int(280 * scale_factor))
        message_label.pack(pady=(int(5 * scale_factor), int(10 * scale_factor)))

        button_frame = tk.Frame(overlay_frame, bg="#333333")
        button_frame.pack(pady=(int(5 * scale_factor), int(10 * scale_factor)))

        def close_overlay():
            blocker.destroy()
            overlay_frame.destroy()

        if show_options:
            folder_button = tk.Button(
                button_frame, 
                text="From Folder", 
                relief="flat", 
                command=lambda: [on_folder_click(), close_overlay()],
                bg='#ce9c00', 
                fg='#ffffff', 
                activebackground='#977200', 
                activeforeground='#ffffff',
                padx=int(20 * scale_factor), pady=int(10 * scale_factor), font=('Arial', int(12 * scale_factor), 'italic', 'bold')
            )
            folder_button.pack(side=tk.LEFT, padx=int(10 * scale_factor))

            zip_button = tk.Button(
                button_frame, 
                text="From .Zip", 
                relief="flat",
                command=lambda: [on_zip_click(), close_overlay()],
                bg='#ce6200', 
                fg='#ffffff', 
                activebackground='#934601', 
                activeforeground='#ffffff',
                padx=int(30 * scale_factor), pady=int(10 * scale_factor), font=('Arial', int(12 * scale_factor), 'italic', 'bold')
            )
            zip_button.pack(side=tk.LEFT, padx=int(10 * scale_factor))

            back_button_frame = tk.Frame(overlay_frame, bg="#333333")
            back_button_frame.pack(pady=(int(10 * scale_factor), 0))

            back_button = tk.Button(
                back_button_frame, 
                text="Close",
                relief="flat",
                command=close_overlay,
                bg="#808080", 
                fg="#FFFFFF", 
                activebackground="#666666", 
                activeforeground="#FFFFFF",
                padx=int(20 * scale_factor), pady=int(4 * scale_factor), font=('Arial', int(10 * scale_factor), 'bold')
            )
            back_button.pack(pady=(0, 0))
        elif show_confirmation:
            confirm_button = tk.Button(
                button_frame, 
                text="Confirm",
                relief="flat",
                command=lambda: [on_confirm(), close_overlay()],
                bg="#19D719", 
                fg="#FFFFFF", 
                activebackground="#128A12", 
                activeforeground="#FFFFFF",
                font=("Arial", int(10 * scale_factor), "bold"),
                width=int(12 * scale_factor)
            )
            confirm_button.pack(side=tk.LEFT, padx=int(10 * scale_factor))

            cancel_button = tk.Button(
                button_frame,
                text="Cancel",
                relief="flat",
                command=close_overlay,
                bg="#F02D7D",
                fg="#FFFFFF",
                activebackground="#D71C19",
                activeforeground="#FFFFFF",
                font=("Arial", int(10 * scale_factor), "bold"),
                width=int(12 * scale_factor)
            )
            cancel_button.pack(side=tk.LEFT, padx=int(10 * scale_factor))
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

    try:
        with open('data/config.json', 'r') as f:
            config = json.load(f)
            backup_folder = config.get('saves_backups', '')
            auto_backups_on = config.get('auto_backups_on', False)
            backups_zip = config.get('backups_zip', False)

    except Exception as e:
        create_overlay("Error", f"Error loading config: {e}")
        return

    if not backup_folder:
        create_overlay("Error", "Backup folder path is not configured in config.json.")
        return

    if game["emulator"] == "Yuzu":
        game_save_path = os.path.join(yuzu_saves, game['id'])
    elif game["emulator"] == "Ryujinx":
        game_save_path = os.path.join(ryujinx_saves, game['id'])
    os.makedirs(game_save_path, exist_ok=True)

    create_overlay("Select Backup Source", "Choose the source to restore from:", show_options=True)

    def perform_auto_backup():
        if auto_backups_on and os.path.exists(game_save_path) and os.listdir(game_save_path):
            timestamp = datetime.now().strftime("%Y.%m.%d @ %H.%M.%S")
            if game["emulator"] == "Yuzu":
                auto_backup_path = os.path.join(yuzu_saves, "__backups__", game['id'], timestamp)
            elif game["emulator"] == "Ryujinx":
                auto_backup_path = os.path.join(ryujinx_saves, "__backups__", game['id'], timestamp)
            os.makedirs(os.path.dirname(auto_backup_path), exist_ok=True)

            try:
                if backups_zip:
                    with zipfile.ZipFile(f"{auto_backup_path}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(game_save_path):
                            for file in files:
                                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), game_save_path))
                            for dir in dirs:
                                folder_path = os.path.join(root, dir)
                                for folder_root, folder_dirs, folder_files in os.walk(folder_path):
                                    for folder_file in folder_files:
                                        zipf.write(os.path.join(folder_root, folder_file), os.path.relpath(os.path.join(folder_root, folder_file), game_save_path))
                else:
                    shutil.copytree(game_save_path, auto_backup_path, dirs_exist_ok=True)
            except Exception as e:
                create_overlay("Error", f"Error during automatic backup: {e}")

    def restore_from_zip(backup_path):
        try:
            perform_auto_backup()
            
            for root, dirs, files in os.walk(game_save_path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir))

            with zipfile.ZipFile(backup_path, 'r') as zip_ref:
                zip_ref.extractall(game_save_path)

            create_overlay("Success", "Backup restored successfully!")

        except Exception as e:
            create_overlay("Error", f"Error restoring the backup: {e}")

    def restore_from_folder(backup_path):
        try:
            perform_auto_backup()
            
            for root, dirs, files in os.walk(game_save_path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir))

            for item in os.listdir(backup_path):
                s = os.path.join(backup_path, item)
                d = os.path.join(game_save_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            create_overlay("Success", "Backup restored successfully!")

        except Exception as e:
            create_overlay("Error", f"Error restoring the backup: {e}")

    def on_zip_click():
        backup_path = filedialog.askopenfilename(
            title="Select a backup file",
            filetypes=[("ZIP Files", "*.zip")],
            initialdir=backup_folder
        )
        if backup_path:
            create_overlay(
                "Confirm Restore",
                "Are you sure you want to restore the backup from the selected .zip file?",
                show_confirmation=True,
                on_confirm=lambda: restore_from_zip(backup_path)
            )

    def on_folder_click():
        backup_path = filedialog.askdirectory(
            title="Select a folder to restore from",
            initialdir=backup_folder
        )
        if backup_path:
            create_overlay(
                "Confirm Restore",
                "Are you sure you want to restore the backup from the selected folder?",
                show_confirmation=True,
                on_confirm=lambda: restore_from_folder(backup_path)
            )
