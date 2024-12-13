import os
import json

def open_emulator_folder(emulator):

    try:
        with open('data/config.json', 'r') as f:
            config = json.load(f)

            if emulator == "Yuzu":
                emulator_folder = config.get('saves_yuzu', '')
            elif emulator == "Ryujinx":
                emulator_folder = config.get('saves_ryujinx', '')

            if os.path.exists(emulator_folder):
                os.startfile(emulator_folder)
            else:
                print("Error", f"Folder not found for emulator: {emulator}")
    except Exception as e:
        print("Error", f"Error opening folder for emulator: {emulator}. Error: {e}")
