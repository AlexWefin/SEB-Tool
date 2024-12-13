import os
import json
import tkinter as tk
from tkinter import messagebox
from app.config.games_manager import load_games
from app.utils.others.app_reloader import reload_app

def delete_game(window, game):

    def show_delete_confirmation_overlay(parent, game, delete_command):
        scale_factor = parent.winfo_height() / 800

        blocker = tk.Frame(parent, bg="#333333")
        blocker.place(relx=0, rely=0, relwidth=1, relheight=1)

        overlay = tk.Frame(
            parent,
            bg="#2B2B2B",
            width=int(300 * scale_factor),
            height=int(150 * scale_factor),
        )
        overlay.place(relx=0.5, rely=0.5, anchor="center")

        bg_color = "#333333"
        fg_color = "#FFFFFF"
        overlay.configure(bg=bg_color)

        title_label = tk.Label(
            overlay,
            text="Confirm Decision",
            font=("Arial", int(14 * scale_factor), "bold"),
            fg=fg_color,
            bg=bg_color,
        )
        title_label.pack(pady=(int(10 * scale_factor), int(5 * scale_factor)))

        message = f"Are you sure you want to delete the game '{game['name']}'?"
        message_label = tk.Label(
            overlay,
            text=message,
            wraplength=int(250 * scale_factor),
            bg=bg_color,
            fg=fg_color,
            font=("Arial", int(12 * scale_factor)),
        )
        message_label.pack(pady=(int(5 * scale_factor), int(10 * scale_factor)))

        button_frame = tk.Frame(overlay, bg=bg_color)
        button_frame.pack(pady=(int(10 * scale_factor), int(10 * scale_factor)))

        def on_confirm():
            delete_command()
            blocker.destroy()
            overlay.destroy()
            messagebox.showinfo(
                "Success", f"The game '{game['name']}' was deleted successfully."
            )

        button_width = int(12 * scale_factor)

        yes_button = tk.Button(
            button_frame,
            text="Yes",
            command=on_confirm,
            bg="#19D719",
            fg="white",
            relief="flat",
            font=("Arial", int(10 * scale_factor), "bold"),
            width=button_width,
        )
        yes_button.pack(side=tk.LEFT, padx=int(10 * scale_factor))

        no_button = tk.Button(
            button_frame,
            text="No",
            command=lambda: [blocker.destroy(), overlay.destroy()],
            bg="#F02D7D",
            fg="white",
            relief="flat",
            font=("Arial", int(10 * scale_factor), "bold"),
            width=button_width,
        )
        no_button.pack(side=tk.LEFT, padx=int(10 * scale_factor))

    def confirm_delete():
        games = load_games()
        games = [g for g in games if not (g['id'] == game['id'] and g['emulator'] == game['emulator'])]

        with open("data/games.json", "w", encoding="utf-8") as file:
            json.dump(games, file, indent=4, ensure_ascii=False)

        image_path = f"assets/icons/games/{game['id']}_{game['emulator']}.png"
        if os.path.exists(image_path):
            os.remove(image_path)

        reload_app()

    show_delete_confirmation_overlay(window, game, confirm_delete)
