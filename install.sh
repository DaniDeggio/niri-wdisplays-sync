#!/bin/bash

# Directories
NIRI_DIR="$HOME/.config/niri"
SYSTEMD_DIR="$HOME/.config/systemd/user"

# Create directories if they do not exist
mkdir -p "$NIRI_DIR/cfg"
mkdir -p "$SYSTEMD_DIR"

# Copy python script
echo "Installing niri-wdisplays-sync.py in $NIRI_DIR..."
cp niri-wdisplays-sync.py "$NIRI_DIR/"
chmod +x "$NIRI_DIR/niri-wdisplays-sync.py"

# Install CLI tool
echo "Installing niri-wallpaper CLI in $HOME/.local/bin..."
mkdir -p "$HOME/.local/bin"
cp niri-wallpaper.py "$HOME/.local/bin/niri-wallpaper"
chmod +x "$HOME/.local/bin/niri-wallpaper"

# Copy systemd services
echo "Installing systemd services in $SYSTEMD_DIR..."
cp niri-wdisplays-sync.service "$SYSTEMD_DIR/"
cp linux-wallpaperengine.service "$SYSTEMD_DIR/"

# Reload systemd and enable services
echo "Reloading and enabling systemd services..."
systemctl --user daemon-reload
systemctl --user enable --now niri-wdisplays-sync.service
systemctl --user enable --now linux-wallpaperengine.service

echo ""
echo "=== INSTALLATION COMPLETE ==="
echo "Make sure your $NIRI_DIR/config.kdl file includes the line:"
echo 'include "./cfg/display.kdl"'
echo "and remove any old hardware configurations (output blocks) present in the main config file."
