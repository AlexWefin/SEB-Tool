import os
import tkinter as tk
from PIL import Image, ImageTk

from app.utils.backup_system.create_backups import create_backup
from app.utils.backup_system.install_backups import install_backup
from app.interface.ui_settings.game_settings import game_settings
from app.utils.open_folder import open_emulator_folder
from app.utils.delete_game import delete_game

def game_info(window, game, saves_yuzu, saves_ryujinx, saves_backup):
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    if screen_width <= 800 and screen_height <= 600:
        scale_factor = 0.6
    elif screen_width <= 1366 and screen_height <= 768:
        scale_factor = 0.8
    elif screen_width <= 1920 and screen_height <= 1080:
        scale_factor = 1
    elif screen_width <= 2560 and screen_height <= 1440:
        scale_factor = 1.2
    else:
        scale_factor = 1.5

    def apply_scale_factor(size, scale_factor):
        return int(size * scale_factor)


    if hasattr(window, 'overlay_frame') and window.overlay_frame.winfo_exists():
        window.overlay_frame.destroy()

    overlay_frame = tk.Frame(window, bg="#333333", width=apply_scale_factor(350, scale_factor))
    overlay_frame.place(relx=1.0, rely=0.0, anchor="ne", relheight=1.0)
    window.overlay_frame = overlay_frame

    icon_path = f"assets/icons/games/{game['id']}_{game['emulator']}.png"
    if not os.path.exists(icon_path):
        icon_path = "assets/icons/system/no_game_image.png"

    img = Image.open(icon_path).convert("RGBA") 
    img = img.resize((apply_scale_factor(350, scale_factor), apply_scale_factor(350, scale_factor)))
    img_label = ImageTk.PhotoImage(img)
    img_label_widget = tk.Label(overlay_frame, image=img_label, bg="#333333")
    img_label_widget.image = img_label
    img_label_widget.pack(pady=(0, apply_scale_factor(10, scale_factor)))

    rectangle_width = apply_scale_factor(350, scale_factor)
    rectangle_height = apply_scale_factor(30, scale_factor)
    bg_color = "#333333"
    font_color = "#FFFFFF"
    max_font_size = apply_scale_factor(15, scale_factor)

    rectangle_canvas = tk.Canvas(overlay_frame, width=rectangle_width, height=rectangle_height, bg=bg_color, highlightthickness=0)
    rectangle_canvas.pack()

    truncated_name = game['name']
    font_size = max_font_size

    while True:
        font = ("Arial", font_size, "italic")
        temp_label = tk.Label(rectangle_canvas, text=truncated_name, font=font)
        temp_label.update_idletasks()

        if temp_label.winfo_reqwidth() <= rectangle_width or font_size <= 6:
            break
        font_size -= 1

    name_label = tk.Label(rectangle_canvas, text=truncated_name, font=font, fg=font_color, bg=bg_color)
    name_label.place(relx=0.5, rely=0.5, anchor="center")

    rectangle_height = apply_scale_factor(20, scale_factor)
    font_color = "gray"
    max_font_size = apply_scale_factor(11, scale_factor)

    id_canvas = tk.Canvas(overlay_frame, width=rectangle_width, height=rectangle_height, bg=bg_color, highlightthickness=0)
    id_canvas.pack(pady=(2, 5))

    truncated_id = game['id'][:40] + ("..." if len(game['id']) > 40 else "")
    font_size = max_font_size

    while True:
        font = ("Arial", font_size)
        temp_label = tk.Label(id_canvas, text=truncated_id, font=font)
        temp_label.update_idletasks()

        if temp_label.winfo_reqwidth() <= rectangle_width or font_size <= 6:
            break
        font_size -= 1

    id_label = tk.Label(id_canvas, text=truncated_id, font=font, fg=font_color, bg=bg_color)
    id_label.place(relx=0.5, rely=0.5, anchor="center")

    rectangle_height = apply_scale_factor(20, scale_factor)
    max_font_size = apply_scale_factor(9, scale_factor)

    backup_canvas = tk.Canvas(overlay_frame, width=rectangle_width, height=rectangle_height, bg=bg_color, highlightthickness=0)
    backup_canvas.pack(pady=(0, apply_scale_factor(10, scale_factor)))

    truncated_backup_name = game['emulator'][:44] + ("..." if len(game['emulator']) > 44 else "")
    font_size = max_font_size

    while True:
        font = ("Arial", font_size)
        temp_label = tk.Label(backup_canvas, text=truncated_backup_name, font=font)
        temp_label.update_idletasks()

        if temp_label.winfo_reqwidth() <= rectangle_width or font_size <= 6:
            break
        font_size -= 1

    backup_name_label = tk.Label(backup_canvas, text=truncated_backup_name, font=font, fg=font_color, bg=bg_color)
    backup_name_label.place(relx=0.5, rely=0.5, anchor="center")

    button_frame = tk.Frame(overlay_frame, bg="#333333")
    button_frame.pack(pady=(apply_scale_factor(90, scale_factor), apply_scale_factor(10, scale_factor)))

    install_backup_button = tk.Button(
        button_frame,
        text="Install Backup",
        relief="flat",
        command=lambda: install_backup(window, game, saves_yuzu, saves_ryujinx),
        bg="#F02D7D", 
        fg="#FFFFFF",
        font=("Arial", apply_scale_factor(12, scale_factor), "italic", "bold"),
        activebackground="#D21C68",
        activeforeground="#FFFFFF",
        width=apply_scale_factor(22, scale_factor),
        padx=apply_scale_factor(10, scale_factor),
        pady=apply_scale_factor(4, scale_factor)
    )

    create_backup_button = tk.Button(
        button_frame,
        text="Create New Backup",
        relief="flat",
        command=lambda: create_backup(window, game, saves_yuzu, saves_ryujinx, saves_backup),
        bg="#19D719", 
        fg="#FFFFFF",
        font=("Arial", apply_scale_factor(12, scale_factor), "italic", "bold"),
        activebackground="#17C717",
        activeforeground="#FFFFFF",
        width=apply_scale_factor(22, scale_factor),
        padx=apply_scale_factor(10, scale_factor),
        pady=apply_scale_factor(4, scale_factor)
    )

    install_backup_button.pack(fill=tk.X, pady=(5, 5))
    create_backup_button.pack(fill=tk.X, pady=(5, 5))

    emoji_frame = tk.Frame(overlay_frame, bg="#333333")
    emoji_frame.place(relx=0.5, rely=0.90, anchor="n")

    placeholder_label = tk.Label(emoji_frame, text="ㅤ", font=("Arial", apply_scale_factor(16, scale_factor)), fg="white", bg="#333333")
    placeholder_label.pack(side=tk.LEFT, padx=0)

    emoji_name_backup = tk.Label(emoji_frame, text="📝", font=("Arial", apply_scale_factor(15, scale_factor)), fg="white", bg="#333333")
    emoji_name_backup.pack(side=tk.LEFT, padx=0)
    emoji_name_backup.bind("<Button-1>", lambda e: game_settings(window, game))

    emoji_folder = tk.Label(emoji_frame, text="📁", font=("Arial", apply_scale_factor(16, scale_factor)), fg="white", bg="#333333")
    emoji_folder.pack(side=tk.LEFT, padx=20)
    emoji_folder.bind("<Button-1>", lambda e: open_emulator_folder(game['emulator']))

    emoji_delete_game = tk.Label(emoji_frame, text="🗑️", font=("Arial", apply_scale_factor(15, scale_factor)), fg="white", bg="#333333")
    emoji_delete_game.pack(side=tk.LEFT, padx=0)
    emoji_delete_game.bind("<Button-1>", lambda e, g=game: delete_game(window, g))

    close_button_widget = tk.Label(overlay_frame, text="⇤", bg="#333333", fg="#FFFFFF", font=("Arial", apply_scale_factor(26, scale_factor)))
    close_button_widget.place(relx=0.01, rely=1.01, anchor="sw")

    def close_overlay(event):
        overlay_frame.place_forget()

    close_button_widget.bind("<Button-1>", close_overlay)
