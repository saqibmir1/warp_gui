#!/usr/bin/env python
import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                             QPushButton, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont


class VPNApp(QWidget):
    def __init__(self):
        super().__init__()
        self.is_connected = False
        self.init_ui()
        
        # Setup timer for automatic status updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_vpn_status)
        self.timer.start(2000)  # Update every 2 seconds
        
    def init_ui(self):
        self.setWindowTitle('Cloudflare WARP VPN')
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #1E88E5;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        self.title_label = QLabel('WARP VPN', alignment=Qt.AlignCenter)
        self.title_label.setFont(QFont('Segoe UI', 24, QFont.Bold))
        self.title_label.setStyleSheet('color: #1E88E5; margin-bottom: 10px;')
        main_layout.addWidget(self.title_label)
        
        # Status card
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #E0E0E0;
            }
        """)
        status_layout = QVBoxLayout(status_frame)
        
        status_title = QLabel('Status')
        status_title.setFont(QFont('Segoe UI', 14))
        status_layout.addWidget(status_title)
        
        self.status_label = QLabel('Checking...')
        self.status_label.setFont(QFont('Segoe UI', 18, QFont.Bold))
        status_layout.addWidget(self.status_label)
        
        # Add detailed status
        self.detail_label = QLabel('')
        self.detail_label.setFont(QFont('Segoe UI', 10))
        self.detail_label.setWordWrap(True)
        status_layout.addWidget(self.detail_label)
        
        main_layout.addWidget(status_frame)
        
        # Toggle button
        self.toggle_button = QPushButton('Connect')
        self.toggle_button.setFont(QFont('Segoe UI', 12))
        self.toggle_button.setMinimumHeight(50)
        self.toggle_button.clicked.connect(self.toggle_vpn)
        main_layout.addWidget(self.toggle_button)
        
        # Bottom info
        info_layout = QHBoxLayout()
        
        self.update_status_label = QLabel('Auto-updating...')
        self.update_status_label.setFont(QFont('Segoe UI', 9))
        self.update_status_label.setStyleSheet('color: #757575;')
        info_layout.addWidget(self.update_status_label, alignment=Qt.AlignLeft)
        
        main_layout.addLayout(info_layout)
        
        self.setLayout(main_layout)
        
        # Initial status update
        self.update_vpn_status()
        
    def update_vpn_status(self):
        try:
            result = subprocess.run(['warp-cli', 'status'], stdout=subprocess.PIPE, text=True)
            status_output = result.stdout.strip()
            
            self.detail_label.setText(status_output)
            
            if "Connected" in status_output:
                self.is_connected = True
                self.status_label.setText('Connected')
                self.status_label.setStyleSheet('color: #43A047;')  # Green
                self.toggle_button.setText('Disconnect')
                self.toggle_button.setStyleSheet("""
                    QPushButton {
                        background-color: #F44336;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 10px 20px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #E53935;
                    }
                    QPushButton:pressed {
                        background-color: #D32F2F;
                    }
                """)
            else:
                self.is_connected = False
                self.status_label.setText('Disconnected')
                self.status_label.setStyleSheet('color: #757575;')  # Gray
                self.toggle_button.setText('Connect')
                self.toggle_button.setStyleSheet("""
                    QPushButton {
                        background-color: #1E88E5;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 10px 20px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                    QPushButton:pressed {
                        background-color: #1565C0;
                    }
                """)
                
            self.update_status_label.setText(f'Last updated: {self.current_time()}')
        except Exception as e:
            self.detail_label.setText(f"Error: {str(e)}")
        
    def toggle_vpn(self):
        self.toggle_button.setDisabled(True)
        self.status_label.setText('Processing...')
        self.status_label.setStyleSheet('color: #FF9800;')  # Orange
        
        try:
            if not self.is_connected:
                # Execute the 'warp-cli connect' command
                subprocess.run(['warp-cli', 'connect'], stdout=subprocess.PIPE)
            else:
                # Execute the 'warp-cli disconnect' command
                subprocess.run(['warp-cli', 'disconnect'], stdout=subprocess.PIPE)
                
            # Update status after a short delay to allow the VPN to connect/disconnect
            QTimer.singleShot(1000, self.update_vpn_status)
        except Exception as e:
            self.detail_label.setText(f"Error: {str(e)}")
        
        self.toggle_button.setDisabled(False)
    
    def current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    vpn_app = VPNApp()
    vpn_app.show()
    sys.exit(app.exec_())
