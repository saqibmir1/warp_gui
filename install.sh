#!/bin/sh

sudo pacman -S python-pyqt5 --needed --noconfirm || sudo apt install python3-pyqt5 || echo "Couldnt install pyqt5: Manual installation required"

APP_DIR=$HOME/.local/share/applications/warp_gui
mkdir -p $APP_DIR
cp warp_gui.py $APP_DIR
cp warp_gui.png $APP_DIR


cat <<EOT >> $HOME/.local/share/applications/warp_gui/warp_gui.desktop
[Desktop Entry]
Version=1.0
Exec=$HOME/.local/share/applications/warp_gui/warp_gui.py
Icon=$HOME/.local/share/applications/warp_gui/warp_gui.png
Name=WARP GUI
Type=Application
EOT

echo "Installation Finished"