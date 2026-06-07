# Niri Wdisplays Sync

This tool bridges the gap between `wdisplays` and **Niri** (Wayland compositor), making dynamically generated display layouts permanent, while also ensuring seamless integration with **linux-wallpaperengine**.

## The Problem
When you disconnect or swap a monitor, Niri resets the layout or applies its default one. Furthermore, `linux-wallpaperengine` requires port names (`DP-1`, etc.) to work correctly. If these ports are swapped, the wallpapers get assigned to the wrong physical screens.

## The Solution
This Python daemon solves both issues:
1. It saves the position, resolution, and configuration of each screen (based on its unique EDID hardware identifier, totally independent of the port!).
2. If a monitor is disconnected, the daemon remembers it. When you plug it back into any port, it instantly snaps back to its saved position.
3. It maps each hardware monitor to a specific wallpaper ID and dynamically regenerates the correct command for `linux-wallpaperengine` on the fly, regardless of which physical port the screen is connected to!

## Installation
Clone the repository and run the installation script:
```bash
chmod +x install.sh
./install.sh
```

## Wallpaper Configuration
You no longer need to edit Python scripts or note down hardware EDIDs manually! A handy CLI tool is included:

- List connected screens and their assignments:
  ```bash
  niri-wallpaper list
  ```
- Browse your downloaded Steam Workshop wallpapers:
  ```bash
  niri-wallpaper wallpapers
  ```
- Assign a Steam Workshop wallpaper ID to a screen by its port (e.g. DP-1):
  ```bash
  niri-wallpaper set DP-1 3373381434
  ```

The tool will automatically resolve the physical port to its permanent hardware EDID identifier, save the assignment, and restart the daemon so the new wallpaper appears instantly!
