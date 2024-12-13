import os
import json
import tempfile
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

from app.utils.others.app_reloader import reload_app
from app.utils.others.app_dark_bar import dark_title_bar
from app.config.config_manager import load_log
from app.config.path_manager import configure_yuzu_folder, configure_ryujinx_folder
from app.config.games_manager import GAMES_FILE

def game_settings(window, game):
    scale_factor = window.winfo_height() / 800

    is_maximized = window.state() == "zoomed"

    if hasattr(window, "settings_game_popup") and window.settings_game_popup.winfo_exists():
        messagebox.showinfo("Info", "The 'Game Settings' window is already open.")
        return

    popup = tk.Toplevel(window)
    popup.title("Edit Game Settings")
    popup.iconbitmap("assets/icons/app/app.ico")

    window_width = int(400 * scale_factor)
    window_height = int(700 * scale_factor)
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    position_top = int(screen_height / 2 - window_height / 2) - int(50 * scale_factor)
    position_left = int(screen_width / 2 - window_width / 2)

    popup.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
    popup.resizable(False, False)
    popup.grab_set()

    bg_color = "#2B2B2B"
    fg_color = "#FFFFFF"
    popup.configure(bg=bg_color)

    dark_title_bar(popup)

    icon_path = f"assets/icons/games/{game['id']}_{game['emulator']}.png"
    if not os.path.exists(icon_path):
        icon_path = "assets/icons/system/no_game_image.png"

    img = Image.open(icon_path).resize((400, 400))
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(popup, image=img, bg=bg_color)
    img_label.image = img
    img_label.pack(pady=(int(10 * scale_factor), int(2 * scale_factor)))

    temp_image_path = None

    def change_image():
        nonlocal temp_image_path

        response = messagebox.askyesno("Confirmation", "Would you like to update the game's image?")
        if response:
            image_path = filedialog.askopenfilename(
                title="Select an image", 
                filetypes=[("All Image Files", "*.*")]
            )
            if image_path:
                try:
                    image = Image.open(image_path)
                    image = image.resize((400, 400))
                    temp_image_path = tempfile.mktemp(suffix=".png")
                    image.save(temp_image_path, "PNG")

                    update_image()
                except Exception as e:
                    messagebox.showerror("Error", f"{e}")

    def update_image():
        try:
            if temp_image_path and os.path.exists(temp_image_path):
                img = Image.open(temp_image_path)
                img = img.resize((400, 400))
                img = ImageTk.PhotoImage(img)
            else:
                img = Image.open("assets/icons/system/no_game_image.png").resize((400, 400))
                img = ImageTk.PhotoImage(img)
            img_label.configure(image=img)
            img_label.image = img
        except Exception as e:
            print(f"Error updating the image: {e}")

    img_label.bind("<Button-1>", lambda e: change_image())

    font_size = int(12 * scale_factor)

    tk.Label(popup, text="Game Name:", bg=bg_color, fg=fg_color, font=("Arial", font_size)).pack(pady=int(5 * scale_factor))
    name_entry = tk.Entry(popup, width=int(30 * scale_factor))
    name_entry.insert(0, game['name'])
    name_entry.pack()

    tk.Label(popup, text="Game ID:", bg=bg_color, fg=fg_color, font=("Arial", font_size)).pack(pady=int(5 * scale_factor))
    id_entry = tk.Entry(popup, width=int(30 * scale_factor))
    id_entry.insert(0, game['id'])
    id_entry.pack()

    tk.Label(popup, text="Emulator:", bg=bg_color, fg=fg_color, font=("Arial", font_size)).pack(pady=int(5 * scale_factor))
    emulator_display_options = ["Yuzu", "Ryujinx"]
    emulator_options = {
        "Yuzu": "Yuzu",
        "Ryujinx": "Ryujinx"
    }

    emulator_combo = ttk.Combobox(popup, values=emulator_display_options, state="readonly", width=int(30 * scale_factor))
    emulator_current = game.get('emulator', 'Yuzu')
    emulator_combo.set(emulator_current)
    emulator_combo.pack()

    def save_game(name, game_id, emulator):
        games = load_games()
        for g in games:
            if g['id'] == game['id'] and g['emulator'] == game['emulator']:
                g.update({
                    "name": name,
                    "id": game_id,
                    "emulator": emulator
                })
        with open(GAMES_FILE, "w", encoding="utf-8") as file:
            json.dump(games, file, indent=4, ensure_ascii=False)

    def load_games():
        try:
            with open(GAMES_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        

    def save():
        name = name_entry.get().strip()
        game_id = id_entry.get().strip()
        emulator_display = emulator_combo.get()
        emulator = emulator_options[emulator_display]

        config_data = load_log()
        saves_yuzu = config_data.get('saves_yuzu', '')
        saves_ryujinx = config_data.get('saves_ryujinx', '')

        if emulator == "Yuzu" and not saves_yuzu:
            if not configure_yuzu_folder():
                return
        elif emulator == "Ryujinx" and not saves_ryujinx:
            if not configure_ryujinx_folder():
                return

        def proceed_with_save_game():
            games = load_games()
            for g in games:
                if g['id'] == game_id and g['emulator'] == emulator and g != game:
                    error_message = f"The ID '{game_id}' is already assigned to another game on emulator '{emulator}'!"
                    messagebox.showwarning("Error", error_message)
                    return

            old_image_path = f"assets/icons/games/{game['id']}_{game['emulator']}.png"
            new_image_path = f"assets/icons/games/{game_id}_{emulator}.png"

            if temp_image_path:
                if os.path.exists(new_image_path):
                    os.remove(new_image_path)
                os.rename(temp_image_path, new_image_path)
            elif os.path.exists(old_image_path) and old_image_path != new_image_path:
                if os.path.exists(new_image_path):
                    os.remove(new_image_path)
                os.rename(old_image_path, new_image_path)

            save_game(name, game_id, emulator)
            messagebox.showinfo("Success", f"Settings for game '{name}' were saved successfully.")

            popup.destroy()
            if is_maximized:
                window.state("zoomed")
            else:
                window.deiconify()
            reload_app()

        def validate_game_id(game_id, emulator):
            if emulator == "Ryujinx":
                return game_id.startswith("0000000000") and len(game_id) == 16
            elif emulator == "Yuzu":
                return len(game_id) == 16 and not game_id.startswith("0x") and game_id.isalnum()
            return True

        def show_ryujinx_warning():
            messagebox.showwarning(
                "Invalid ID",
                "The ID you entered might not be correct for Ryujinx.\n\n"
                "Example of a valid ID: 0000000000000001\n\n"
                "If you need help finding the correct ID, click 'Yes' to learn more."
            )
            if messagebox.askyesno("More Info", "If you need help finding the correct ID, click 'Yes' to learn more."):
                webbrowser.open("https://github.com/AlexWefin/SEB-Tool/tree/main?tab=readme-ov-file#ryujinx")

        def show_yuzu_warning():
            messagebox.showwarning(
                "Invalid ID",
                "The ID you entered might not be correct for Yuzu.\n\n"
                "Example of a valid ID: 010062B01525C000\n\n"
                "Make sure the ID does not include '0x' shown in the Yuzu interface."
            )
            if messagebox.askyesno("More Info", "If you need help finding the correct ID, click 'Yes' to learn more."):
                webbrowser.open("https://github.com/AlexWefin/SEB-Tool/blob/main/README.md#yuzu")

        def show_yuzu_zero_warning(proceed_callback):
            result = messagebox.askyesno(
                "Attention",
                "The ID you entered looks more like a Ryujinx ID.\n\n"
                "Do you want to proceed?"
            )
            if result:
                proceed_callback()

        if name and game_id:
            if emulator == "Ryujinx" and not validate_game_id(game_id, emulator):
                show_ryujinx_warning()
            elif emulator == "Yuzu":
                if len(game_id) == 16 and game_id.startswith("0000000000"):
                    show_yuzu_zero_warning(proceed_with_save_game)
                elif not validate_game_id(game_id, emulator):
                    show_yuzu_warning()
                else:
                    proceed_with_save_game()
            else:
                proceed_with_save_game()
        else:
            messagebox.showwarning("Error", "Please fill out all fields.")

    button_style = {
        "bg": "#19D719", 
        "fg": "#FFFFFF",
        "relief": "flat",
        "font": ("Arial", font_size, "bold"),
        "activebackground": "#128A12",
        "activeforeground": "#FFFFFF"
    }

    save_button = tk.Button(popup, text="Save Configuration", command=save, **button_style)
    save_button.pack(pady=int(20 * scale_factor))

    def check_fields():
        if name_entry.get().strip() and id_entry.get().strip() and emulator_combo.get():
            save_button.config(state="normal")
        else:
            save_button.config(state="disabled")

    check_fields()

    name_entry.bind("<KeyRelease>", lambda e: check_fields())
    id_entry.bind("<KeyRelease>", lambda e: check_fields())
    emulator_combo.bind("<<ComboboxSelected>>", lambda e: check_fields())
