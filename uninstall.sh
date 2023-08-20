sudo pacman -Rns python-pyqt-5 || sudo apt install python3-pyqt5 || echo "Could not uninstall pyqt5: Manual intervention required"
rm -rf $HOME/.local/share/applications/warp_gui && 
echo "Uninstallation finished"