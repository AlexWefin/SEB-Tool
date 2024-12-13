import os
import tkinter as tk
from tkinter import messagebox
import json

from app.config.config_manager import load_log, save_log
from app.utils.others.app_reloader import reload_app
from app.config.games_manager import load_games
from app.config.path_manager import configure_backup_folder, configure_yuzu_folder, configure_ryujinx_folder

from app.config.config_manager import CONFIG_FILE
from app.config.games_manager import GAMES_FILE

def open_config_window(window):
    blocker = tk.Frame(window, bg="#333333")
    blocker.place(relx=0, rely=0, relwidth=1, relheight=1)

    scale_factor = window.winfo_height() / 800
    overlay_frame = tk.Frame(window, bg="#2B2B2B", width=int(400 * scale_factor), height=int(500 * scale_factor))
    overlay_frame.place(relx=0.5, rely=0.5, anchor="center")
    bg_color = "#333333"
    fg_color = "#FFFFFF"
    overlay_frame.configure(bg=bg_color)

    title_label = tk.Label(overlay_frame, text="App Settings", font=("Arial", int(14 * scale_factor), "bold"), fg=fg_color, bg=bg_color)
    title_label.pack(pady=(int(10 * scale_factor), int(10 * scale_factor)))

    config_data = load_log()
    saves_yuzu = config_data.get("saves_yuzu", "")
    saves_ryujinx = config_data.get("saves_ryujinx", "")
    saves_backups = config_data.get("saves_backups", "")
    auto_backups_on = config_data.get("auto_backups_on", True)
    auto_backup_name = config_data.get("auto_backup_name", False)
    backups_zip = config_data.get("backups_zip", True)
    
    def update_path_display():
        config_data = load_log()
        saves_yuzu = config_data.get("saves_yuzu", "")
        saves_ryujinx = config_data.get("saves_ryujinx", "")
        saves_backups = config_data.get("saves_backups", "")
        auto_backups_on = config_data.get("auto_backups_on", True)
        auto_backup_name = config_data.get("auto_backup_name", False)
        backups_zip = config_data.get("backups_zip", True)

        yuzu_entry.config(state="normal")
        ryujinx_entry.config(state="normal")
        backup_entry.config(state="normal")
        auto_backups_var.set(auto_backups_on)
        auto_backup_name_var.set(auto_backup_name)
        backups_zip_var.set(backups_zip)

        yuzu_entry.delete(0, tk.END)
        ryujinx_entry.delete(0, tk.END)
        backup_entry.delete(0, tk.END)

        yuzu_entry.insert(0, saves_yuzu)
        ryujinx_entry.insert(0, saves_ryujinx)
        backup_entry.insert(0, saves_backups)

        yuzu_entry.config(state="disabled")
        ryujinx_entry.config(state="disabled")
        backup_entry.config(state="disabled")

    def remove_path_and_games(emulator, entry):
        config_data = load_log()
        games = load_games()

        if emulator == "Yuzu":
            config_data['saves_yuzu'] = ""
        elif emulator == "Ryujinx":
            config_data['saves_ryujinx'] = ""

        games_to_remove = [game for game in games if game['emulator'] == emulator]
        games = [game for game in games if game['emulator'] != emulator]

        for game in games_to_remove:
            icon_path = f"assets/icons/games/{game['id']}_{game['emulator']}.png"
            if os.path.exists(icon_path):
                os.remove(icon_path)

        save_log(config_data['saves_yuzu'], config_data['saves_ryujinx'], config_data['saves_backups'], config_data['auto_backups_on'], config_data['auto_backup_name'], config_data['backups_zip'])

        with open(GAMES_FILE, "w", encoding="utf-8") as file:
            json.dump(games, file, indent=4, ensure_ascii=False)

        reload_app()
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.config(state="disabled")

    def reset_all_configurations():
        show_reset_confirmation_overlay(window, "Restore all Settings", lambda: [reset_config(), reload_app()])

    def reset_config():
        try:
            os.remove(CONFIG_FILE)
            os.remove(GAMES_FILE)
            messagebox.showinfo("Success", "All configurations and game data have been reset.")
        except FileNotFoundError:
            show_error_overlay(window, "Configuration files are missing.")

    def show_remove_confirmation_overlay(parent, emulator, entry):
        blocker = tk.Frame(parent, bg="#333333")
        blocker.place(relx=0, rely=0, relwidth=1, relheight=1)

        overlay = tk.Frame(parent, bg="#2B2B2B", width=300, height=150)
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        bg_color = "#333333"
        fg_color = "#FFFFFF"
        overlay.configure(bg=bg_color)

        title_label = tk.Label(overlay, text="Confirmation", font=("Arial", 14, "bold"), fg=fg_color, bg=bg_color)
        title_label.pack(pady=(10, 5))

        message = f"Are you sure you want to remove '{emulator}'?"
        message_label = tk.Label(overlay, text=message, wraplength=250, bg=bg_color, fg=fg_color)
        message_label.pack(pady=(5, 10))

        button_frame = tk.Frame(overlay, bg=bg_color)
        button_frame.pack(pady=(10, 10))

        confirm_button = tk.Button(button_frame, text="Confirm", command=lambda: [remove_path_and_games(emulator, entry), blocker.destroy(), overlay.destroy()], bg="#19D719", fg="white", relief="flat")
        confirm_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=lambda: [blocker.destroy(), overlay.destroy()], bg="#F02D7D", fg="white", relief="flat")
        cancel_button.pack(side=tk.LEFT, padx=5)

    def show_reset_confirmation_overlay(parent, title, action_command):
        blocker = tk.Frame(parent, bg="#333333")
        blocker.place(relx=0, rely=0, relwidth=1, relheight=1)

        overlay = tk.Frame(parent, bg="#2B2B2B", width=300, height=150)
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        bg_color = "#333333"
        fg_color = "#FFFFFF"
        overlay.configure(bg=bg_color)

        title_label = tk.Label(overlay, text="Confirmation", font=("Arial", 14, "bold"), fg=fg_color, bg=bg_color)
        title_label.pack(pady=(10, 5))

        message = "Are you certain you want to reset all configurations? This will delete all settings and game data but will not affect your saved game files."
        tk.Label(overlay, text=message, wraplength=250, bg=bg_color, fg=fg_color).pack(pady=(5, 10))

        button_frame = tk.Frame(overlay, bg=bg_color)
        button_frame.pack(pady=(10, 10))

        confirm_button = tk.Button(button_frame, text="Confirm", command=lambda: [action_command(), blocker.destroy(), overlay.destroy()], bg="#19D719", fg="white", relief="flat")
        confirm_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=lambda: [blocker.destroy(), overlay.destroy()], bg="#F02D7D", fg="white", relief="flat")
        cancel_button.pack(side=tk.LEFT, padx=5)

    def show_error_overlay(parent, message):
        blocker = tk.Frame(parent, bg="#333333")
        blocker.place(relx=0, rely=0, relwidth=1, relheight=1)

        overlay = tk.Frame(parent, bg="#2B2B2B", width=300, height=150)
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        bg_color = "#333333"
        fg_color = "#FFFFFF"
        overlay.configure(bg=bg_color)

        title_label = tk.Label(overlay, text="Error", font=("Arial", 14, "bold"), fg=fg_color, bg=bg_color)
        title_label.pack(pady=(10, 5))

        tk.Label(overlay, text=message, wraplength=250, bg=bg_color, fg=fg_color).pack(pady=(5, 10))

        close_button = tk.Button(overlay, text="Close", command=lambda: [blocker.destroy(), overlay.destroy()], bg="#808080", fg="white", relief="flat")
        close_button.pack(pady=(10, 10))

    def open_yuzu_path():
        config_data = load_log()
        saves_yuzu = config_data.get("saves_yuzu", "")
        if saves_yuzu:
            os.startfile(saves_yuzu)
        else:
            show_error_overlay(window, "Yuzu path is not configured.")

    def open_ryujinx_path():
        config_data = load_log()
        saves_ryujinx = config_data.get("saves_ryujinx", "")
        if saves_ryujinx:
            os.startfile(saves_ryujinx)
        else:
            show_error_overlay(window, "Ryujinx path is not configured.")

    def open_backup_path():
        config_data = load_log()
        saves_backups = config_data.get("saves_backups", "")
        if saves_backups:
            os.startfile(saves_backups)
        else:
            show_error_overlay(window, "Backup path is not set.")

    def create_path_row(label_text, path, change_command, open_command, remove_command=None):
        row_frame = tk.Frame(overlay_frame, bg=bg_color)
        row_frame.pack(fill=tk.X, pady=(5, 10))

        label = tk.Label(row_frame, text=label_text, bg=bg_color, fg=fg_color)
        label.pack(side=tk.LEFT, padx=(0, 10))

        entry = tk.Entry(row_frame, bg="#4C4C4C", fg="white", width=30, justify="left")
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        entry.insert(0, path)
        entry.config(state="disabled")

        def change_and_reload():
            original_path = entry.get()
            change_command()
            config_data = load_log()
            # Determina a chave correta do caminho de acordo com o label_text
            key_map = {
                "Yuzu Save Path": "saves_yuzu",
                "Ryujinx Save Path": "saves_ryujinx",
                "Backup Save Path": "saves_backups"
            }
            key = key_map.get(label_text, "").lower()
            new_path = config_data.get(key, "")

            if new_path and new_path != original_path:
                update_path_display()
                reload_app()
            else:
                update_path_display()

        change_button = tk.Button(row_frame, text="📝", command=change_and_reload, bg="#19D719", fg="white", relief="flat")
        change_button.pack(side=tk.LEFT, padx=(0, 5))
        open_button = tk.Button(row_frame, text="📂", command=open_command, bg="#f7c302", fg="white", relief="flat")
        open_button.pack(side=tk.LEFT, padx=(0, 5))

        if remove_command:
            def check_and_remove():
                current_path = entry.get()
                if not current_path.strip():
                    if label_text == "Yuzu Save Path":
                        show_error_overlay(window, "Yuzu path is not configured.")
                    elif label_text == "Ryujinx Save Path":
                        show_error_overlay(window, "Ryujinx path is not configured.")
                    else:
                        show_error_overlay(window, f"No path found for {label_text.split()[0]}.")
                else:
                    show_remove_confirmation_overlay(window, label_text.split()[0], remove_command)
            remove_button = tk.Button(row_frame, text="❌", command=check_and_remove, bg="#F02D7D", fg="white", relief="flat")
            remove_button.pack(side=tk.LEFT)

        return entry

    yuzu_entry = create_path_row("Yuzu Save Path", saves_yuzu, configure_yuzu_folder, open_yuzu_path, lambda: remove_path_and_games("Yuzu"))
    ryujinx_entry = create_path_row("Ryujinx Save Path", saves_ryujinx, configure_ryujinx_folder, open_ryujinx_path, lambda: remove_path_and_games("Ryujinx"))
    backup_entry = create_path_row("Backup Save Path", saves_backups, configure_backup_folder, open_backup_path)

    auto_backups_var = tk.BooleanVar(value=auto_backups_on)
    auto_backup_name_var = tk.BooleanVar(value=auto_backup_name)
    backups_zip_var = tk.BooleanVar(value=backups_zip)

    def update_config():
        config_data["auto_backups_on"] = auto_backups_var.get()
        config_data["auto_backup_name"] = auto_backup_name_var.get()
        config_data["backups_zip"] = backups_zip_var.get()

        save_log(config_data['saves_yuzu'], config_data['saves_ryujinx'], 
                config_data['saves_backups'], auto_backups_var.get(), 
                auto_backup_name_var.get(), backups_zip_var.get())
        
        update_path_display()

    auto_backups_check = tk.Checkbutton(overlay_frame, text="Enable Auto Backup on Install", variable=auto_backups_var, command=update_config, bg=bg_color, fg=fg_color, selectcolor="#333333")
    auto_backups_check.pack(pady=(10, 0))

    auto_backup_name_check = tk.Checkbutton(overlay_frame, text="Enable Auto-Naming for Backups", variable=auto_backup_name_var, command=update_config, bg=bg_color, fg=fg_color, selectcolor="#333333")
    auto_backup_name_check.pack(pady=(10, 0))

    backups_zip_check = tk.Checkbutton(overlay_frame, text="Compress Backups into Zip Files", variable=backups_zip_var, command=update_config, bg=bg_color, fg=fg_color, selectcolor="#333333")
    backups_zip_check.pack(pady=(10, 0))

    button_frame = tk.Frame(overlay_frame, bg=bg_color)
    button_frame.pack(pady=(20, 10))

    reset_button = tk.Button(button_frame, text="Restore Settings", command=reset_all_configurations, bg="#F02D7D", fg="white", relief="flat")
    reset_button.pack(fill=tk.X, pady=(0, 5))

    close_button = tk.Button(button_frame, text="Close", command=lambda: [blocker.destroy(), overlay_frame.destroy()], bg="#808080", fg="white", relief="flat", width=8)
    close_button.pack(pady=(0, 0))

    update_path_display()
