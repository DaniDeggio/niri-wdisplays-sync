#!/usr/bin/env python3
import sys
import subprocess
import re
import json
import os

WALLPAPER_CONFIG = os.path.expanduser("~/.config/niri/cfg/wallpapers.json")
STEAM_WORKSHOP_DIR = os.path.expanduser("~/.local/share/Steam/steamapps/workshop/content/431960")

def load_wallpapers():
    if os.path.exists(WALLPAPER_CONFIG):
        try:
            with open(WALLPAPER_CONFIG, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_wallpapers(data):
    with open(WALLPAPER_CONFIG, 'w') as f:
        json.dump(data, f, indent=4)

def get_outputs():
    result = subprocess.run(["niri", "msg", "outputs"], capture_output=True, text=True)
    outputs = []
    current_output = {}
    
    for line in result.stdout.splitlines():
        if line.startswith("Output "):
            if current_output:
                outputs.append(current_output)
            current_output = {}
            m = re.match(r'Output "(.+?)" \((.+?)\)', line)
            if m:
                current_output['name'] = m.group(1)
                current_output['port'] = m.group(2)
                
    if current_output:
        outputs.append(current_output)
        
    return outputs

def list_steam_wallpapers():
    print(f"{'ID SFONDO':<15} | {'TITOLO'}")
    print("-" * 60)
    
    # Prova alcuni percorsi comuni se quello di base non c'è
    dirs_to_check = [
        STEAM_WORKSHOP_DIR,
        os.path.expanduser("~/.steam/steam/steamapps/workshop/content/431960"),
        os.path.expanduser("~/.steam/root/steamapps/workshop/content/431960")
    ]
    
    valid_dir = None
    for d in dirs_to_check:
        if os.path.isdir(d):
            valid_dir = d
            break
            
    if not valid_dir:
        print("Errore: Cartella del Workshop di Steam per Wallpaper Engine non trovata.")
        return
        
    for item in os.listdir(valid_dir):
        path = os.path.join(valid_dir, item, "project.json")
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    title = data.get("title", "Sconosciuto")
                    print(f"{item:<15} | {title}")
            except Exception:
                print(f"{item:<15} | [Errore Lettura File]")

def print_help():
    print("Niri Wallpaper CLI")
    print("Usage:")
    print("  niri-wallpaper list                - Show connected screens and assigned wallpapers")
    print("  niri-wallpaper wallpapers          - List all available Steam Workshop wallpapers and their IDs")
    print("  niri-wallpaper set <port> <id>     - Assign wallpaper <id> to the screen on <port> (e.g. DP-1)")
    print("  niri-wallpaper set <name> <id>     - Assign wallpaper <id> to the screen with hardware <name>")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help", "help"]:
        print_help()
        sys.exit(0)
        
    command = sys.argv[1]
    
    if command == "wallpapers":
        list_steam_wallpapers()
        sys.exit(0)
        
    wallpapers = load_wallpapers()
    outputs = get_outputs()
    
    if command == "list":
        print(f"{'PORT':<10} | {'WALLPAPER ID':<15} | {'HARDWARE NAME'}")
        print("-" * 60)
        for out in outputs:
            name = out['name']
            port = out['port']
            bg = wallpapers.get(name, "None")
            print(f"{port:<10} | {bg:<15} | {name}")
        sys.exit(0)
        
    elif command == "set":
        if len(sys.argv) < 4:
            print("Error: specify the port/name and the wallpaper ID.")
            print("Example: niri-wallpaper set DP-1 3373381434")
            sys.exit(1)
            
        target = sys.argv[2]
        bg_id = sys.argv[3]
        
        # Find matching output by port or exact name
        matched_name = None
        for out in outputs:
            if out['port'] == target or out['name'] == target:
                matched_name = out['name']
                break
                
        if not matched_name:
            matched_name = target
            print(f"Warning: No connected screen matches '{target}'.")
            print(f"The assignment will be saved using '{target}' as the exact hardware name.")
        
        wallpapers[matched_name] = bg_id
        save_wallpapers(wallpapers)
        
        print(f"Wallpaper {bg_id} successfully assigned to '{matched_name}'!")
        print("Restarting the sync daemon to apply changes...")
        subprocess.run(["systemctl", "--user", "restart", "niri-wdisplays-sync.service"])
        print("Done!")
        
    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
