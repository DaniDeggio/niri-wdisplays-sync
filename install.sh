#!/bin/bash

# Directories
NIRI_DIR="$HOME/.config/niri"
SYSTEMD_DIR="$HOME/.config/systemd/user"

# Create directories if they do not exist
mkdir -p "$NIRI_DIR/cfg"
mkdir -p "$SYSTEMD_DIR"

# Copy python script
echo "Installando niri-wdisplays-sync.py in $NIRI_DIR..."
cp niri-wdisplays-sync.py "$NIRI_DIR/"
chmod +x "$NIRI_DIR/niri-wdisplays-sync.py"

# Copy systemd services
echo "Installando i servizi systemd in $SYSTEMD_DIR..."
cp niri-wdisplays-sync.service "$SYSTEMD_DIR/"
cp linux-wallpaperengine.service "$SYSTEMD_DIR/"

# Reload systemd and enable services
echo "Ricaricando e abilitando i servizi systemd..."
systemctl --user daemon-reload
systemctl --user enable --now niri-wdisplays-sync.service
systemctl --user enable --now linux-wallpaperengine.service

echo ""
echo "=== INSTALLAZIONE COMPLETATA ==="
echo "Assicurati che il tuo file $NIRI_DIR/config.kdl includa la riga:"
echo 'include "./cfg/display.kdl"'
echo "e rimuovi le eventuali vecchie configurazioni hardware (output) degli schermi presenti nel file principale."
