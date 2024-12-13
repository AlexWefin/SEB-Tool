import os
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from app.utils.others.app_dark_bar import dark_title_bar
from app.config.config_manager import load_log
from app.config.games_manager import load_games
from app.interface.game_add_window import game_add
from app.interface.game_info_window import game_info
from app.interface.ui_settings.main_settings import open_config_window

def main_window():
    games = load_games()
    config_data = load_log()
    saves_yuzu = config_data.get('saves_yuzu', '')
    saves_ryujinx = config_data.get('saves_ryujinx', '')
    saves_backups = config_data.get('saves_backups', '')

    window = tk.Tk()
    window.title("SEB Tool - Game Library")
    window.iconbitmap("assets/icons/app/app.ico")
    window.attributes('-topmost', 1)
    window.after(10, lambda: window.attributes('-topmost', 0))

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    if screen_width <= 800 or screen_height <= 600:
        scale_factor = 0.6
    elif screen_width <= 1366 or screen_height <= 768:
        scale_factor = 0.8
    elif screen_width <= 1920 or screen_height <= 1080:
        scale_factor = 1
    elif screen_width <= 2560 or screen_height <= 1440:
        scale_factor = 1.2
    else:
        scale_factor = 1.5

    base_width = 1280
    base_height = 720
    window.geometry(f"{int(base_width * scale_factor)}x{int(base_height * scale_factor)}")
    window.resizable(False, False)

    bg_color = "#2B2B2B"
    fg_color = "#FFFFFF"
    window.configure(bg=bg_color)
    dark_title_bar(window)

    window_width = int(base_width * scale_factor)
    window_height = int(base_height * scale_factor)
    position_top = int(screen_height / 2 - window_height / 2) - 50
    position_left = int(screen_width / 2 - window_width / 2)
    window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

    sidebar_width = int(200 * scale_factor)
    sidebar_bg_color = "#333333"
    sidebar = tk.Frame(window, bg=sidebar_bg_color, width=sidebar_width, height=window.winfo_height())
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    canvas = tk.Canvas(window, bg=bg_color, bd=0, highlightthickness=0)
    scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
    content_frame = tk.Frame(canvas, bg=bg_color)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content_frame.bind("<Configure>", on_frame_configure)

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    main_icon_path = "assets/icons/app/app.png"
    if os.path.exists(main_icon_path):
        main_icon_img = PhotoImage(file=main_icon_path).subsample(int(2 / scale_factor), int(2 / scale_factor))
        main_icon_label = tk.Label(sidebar, image=main_icon_img, bg=sidebar_bg_color)
        main_icon_label.image = main_icon_img
        main_icon_label.pack(pady=10)

    add_game_icon_path = "assets/icons/buttons/add_button.png"
    if os.path.exists(add_game_icon_path):
        add_game_icon_img = PhotoImage(file=add_game_icon_path).subsample(int(6 / scale_factor), int(6 / scale_factor))
        spacer = tk.Label(sidebar, bg=sidebar_bg_color)
        spacer.pack(pady=(0, 0))
        add_button = tk.Button(sidebar, image=add_game_icon_img, bg=sidebar_bg_color, bd=0, relief="flat", command=lambda: game_add(window))
        add_button.image = add_game_icon_img
        add_button.pack(pady=(0, 0))

    columns = 6
    game_width = int(200 * scale_factor)
    game_height = int(150 * scale_factor)
    padding = 0
    rows = len(games) // columns
    if len(games) % columns != 0:
        rows += 1

    if rows <= 0:
        content_frame.configure(bg=bg_color)

    def update_scroll():
        total_games = len(games)
        rows = total_games // columns + (1 if total_games % columns else 0)
        if rows > 3:
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.configure(yscrollcommand=scrollbar.set)
        else:
            scrollbar.pack_forget()
            canvas.unbind_all("<MouseWheel>")

    for i, game in enumerate(games):
        row = i // columns
        column = i % columns
        frame = tk.Frame(content_frame, bg="#2b2b2b", pady=10, padx=10, width=game_width, height=game_height)
        frame.grid(row=row, column=column, padx=padding, pady=padding)

        icon_path = f"assets/icons/games/{game['id']}_{game['emulator']}.png"
        if not os.path.exists(icon_path):
            icon_path = "assets/icons/system/no_game_image.png"

        img = Image.open(icon_path).convert("RGBA")

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        if screen_width <= 800 or screen_height <= 600:
            scale_factor = 0.685
            resize_factor = 3.0
        elif screen_width <= 1366 or screen_height <= 768:
            scale_factor = 0.86
            resize_factor = 2.7
        elif screen_width <= 1920 or screen_height <= 1080:
            scale_factor = 1
            resize_factor = 2.35
        elif screen_width <= 2560 or screen_height <= 1440:
            scale_factor = 0.97
            resize_factor = 2.0
        else:
            scale_factor = 1.16
            resize_factor = 1.8

        width, height = img.size
        new_width = int(width / resize_factor * scale_factor)
        new_height = int(height / resize_factor * scale_factor)
        img = img.resize((new_width, new_height), Image.LANCZOS)

        emulator_icon_path = ""
        if game["emulator"] == "Yuzu":
            emulator_icon_path = "assets/icons/emulators/yuzu_emulator.png"
        elif game["emulator"] == "Ryujinx":
            emulator_icon_path = "assets/icons/emulators/ryujinx_emulator.png"

        if os.path.exists(emulator_icon_path):
            emulator_icon = Image.open(emulator_icon_path).convert("RGBA")
            icon_width, icon_height = emulator_icon.size
            scale_ratio = 30 / icon_width
            new_icon_size = (int(icon_width * scale_ratio), int(icon_height * scale_ratio))
            emulator_icon = emulator_icon.resize(new_icon_size, Image.LANCZOS)
            combined_img = Image.new("RGBA", img.size)
            combined_img.paste(img, (0, 0))
            combined_img.paste(emulator_icon, (new_width - new_icon_size[0] - 5, 5), emulator_icon)
            img_resized = combined_img
        else:
            img_resized = img

        img_tk = ImageTk.PhotoImage(img_resized)
        img_label = tk.Label(frame, image=img_tk, bg="#2b2b2b")
        img_label.image = img_tk
        img_label.pack()

        img_label.bind("<Button-1>", lambda e, g=game: game_info(window, g, saves_yuzu, saves_ryujinx, saves_backups))

        rectangle_width = new_width
        rectangle_height = int(20 * scale_factor)

        rectangle_canvas = tk.Canvas(frame, width=rectangle_width, height=rectangle_height, bg="#2b2b2b", highlightthickness=0)
        rectangle_canvas.pack()

        truncated_name = game['name']
        max_font_size = 12
        font_size = max_font_size

        while True:
            font = ("Arial", font_size, "italic")
            temp_label = tk.Label(rectangle_canvas, text=truncated_name, font=font)
            temp_label.update_idletasks()

            if temp_label.winfo_reqwidth() <= rectangle_width or font_size <= 6:
                break
            font_size -= 1

        name_label = tk.Label(rectangle_canvas, text=truncated_name, font=font, fg="#FFFFFF", bg="#2b2b2b")
        name_label.place(relx=0.5, rely=0.5, anchor="center")

        name_label.bind("<Button-1>", lambda e, g=game: game_info(window, g, saves_yuzu, saves_ryujinx, saves_backups))

    update_scroll()

    config_icon_path = "assets/icons/buttons/config_button.png"
    if os.path.exists(config_icon_path):
        config_icon_img = PhotoImage(file=config_icon_path).subsample(int(5/scale_factor), int(5/scale_factor))
        config_button = tk.Button(sidebar, image=config_icon_img, bg=sidebar_bg_color, bd=0, relief="flat", command=lambda: open_config_window(window))
        config_button.image = config_icon_img
        config_button.pack(side=tk.BOTTOM, pady=(10, 10))

    window.mainloop()
