#!/bin/sh

# Try to uninstall PyQt5 using the appropriate package manager
sudo pacman -Rns python-pyqt5 --noconfirm || \
sudo apt remove -y python3-pyqt5 || \
sudo dnf remove -y python3-qt5 || \
echo "Could not uninstall PyQt5: Manual intervention may be required"

# Remove application files and desktop entry
rm -rf "$HOME/.local/share/applications/warp_gui"
rm -f "$HOME/.local/share/applications/warp_gui.desktop"

echo "Uninstallation finished"

