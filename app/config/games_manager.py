import json
import os

GAMES_FILE = os.path.join("data", "games.json")

def load_games():
    if not os.path.exists(GAMES_FILE):
        return []
    try:
        with open(GAMES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_game(name, game_id, emulator):
    games = load_games()
    games.append({"name": name, "id": game_id, "emulator": emulator})
    with open(GAMES_FILE, "w", encoding="utf-8") as file:
        json.dump(games, file, indent=4, ensure_ascii=False)
