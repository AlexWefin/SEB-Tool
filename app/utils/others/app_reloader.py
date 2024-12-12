import sys
import subprocess

def reload_app():
    try:
        script_path = sys.argv[0]
        subprocess.Popen([sys.executable, script_path])
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
