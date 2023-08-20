#!/usr/bin/env python

import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QCheckBox, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class VPNApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Warp VPN GUI')
        self.setGeometry(100, 100, 300, 200)  # Set initial window position and size

        layout = QVBoxLayout()
        
        self.title_label = QLabel('WARP GUI', alignment=Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #1E88E5;')  # Blue color
        layout.addWidget(self.title_label)

        self.label = QLabel('VPN Status:', alignment=Qt.AlignCenter)
        self.label.setStyleSheet('font-size: 18px;')
        layout.addWidget(self.label)

        self.toggle_checkbox = QCheckBox('Toggle VPN')
        self.toggle_checkbox.stateChanged.connect(self.toggle_vpn)
        layout.addWidget(self.toggle_checkbox, alignment=Qt.AlignCenter)

        self.action_button = QPushButton('Refresh')
        self.action_button.clicked.connect(self.update_vpn_status)
        self.action_button.setStyleSheet('font-size: 14px; padding: 5px 20px;')
        layout.addWidget(self.action_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        self.update_vpn_status()

    def update_vpn_status(self):
        result = subprocess.run(['warp-cli', 'status'], stdout=subprocess.PIPE, text=True)
        status_output = result.stdout.strip()
        self.label.setText(f'VPN Status: {status_output}')
        self.toggle_checkbox.setChecked("Connected" in status_output)

    def toggle_vpn(self, state):
        if state == Qt.Checked:
            # Execute the 'warp-cli connect' command
            result = subprocess.run(['warp-cli', 'connect'], stdout=subprocess.PIPE)
        else:
            # Execute the 'warp-cli disconnect' command
            result = subprocess.run(['warp-cli', 'disconnect'], stdout=subprocess.PIPE)

        self.update_vpn_status()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    vpn_app = VPNApp()
    vpn_app.show()
    sys.exit(app.exec_())

