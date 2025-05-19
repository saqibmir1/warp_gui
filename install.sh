#!/bin/sh

# Try to install PyQt5 using the appropriate package manager
sudo pacman -S python-pyqt5 --needed --noconfirm || \
sudo apt install -y python3-pyqt5 || \
sudo dnf install -y python3-qt5 || \
echo "Could not install PyQt5: Manual installation required"

# Set application directory and create it
APP_DIR="$HOME/.local/share/applications/warp_gui"
mkdir -p "$APP_DIR"

# Copy app files
cp warp_gui.py "$APP_DIR"
cp warp_gui.png "$APP_DIR"

# Make sure the main Python file is executable
chmod +x "$APP_DIR/warp_gui.py"

# Create the .desktop file in the correct location
cat <<EOT > "$HOME/.local/share/applications/warp_gui.desktop"
[Desktop Entry]
Version=1.0
Name=WARP GUI
Exec=$APP_DIR/warp_gui.py
Icon=$APP_DIR/warp_gui.png
Type=Application
Categories=Utility;
Terminal=false
EOT

# Make the .desktop file executable
chmod +x "$HOME/.local/share/applications/warp_gui.desktop"

echo "Installation Finished.

