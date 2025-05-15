import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QPushButton, QFileDialog, QTabWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
from typing import List, Tuple, Dict, Any

from app.utils.logger import logger

class SettingsPanelView(QWidget):
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        
        self._config = config
        
        self._init_buttons()
        self._init_ui()
        
        
    def _init_buttons(self):
        """Initialize buttons and their actions."""
        self.nav_settings_btn = QPushButton("Navigation Settings")
        self.nav_settings_btn.setFixedHeight(100)
        self.nav_settings_btn.setFixedWidth(200)
        self.nav_settings_btn.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.ntrip_settings_btn = QPushButton("NTRIP Settings")
        self.ntrip_settings_btn.setFixedHeight(100)
        self.ntrip_settings_btn.setFixedWidth(200)
        self.ntrip_settings_btn.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.other_settings_btn = QPushButton("Other Settings")
        self.other_settings_btn.setFixedHeight(100)
        self.other_settings_btn.setFixedWidth(200)
        self.other_settings_btn.setStyleSheet("font-size: 16px; font-weight: bold;")
        
    def _init_ui(self):
        """Initialize the user interface layout."""
        layout = QHBoxLayout()
        
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(20)
        settings_layout.addWidget(self.nav_settings_btn)
        settings_layout.setSpacing(20)
        settings_layout.addWidget(self.ntrip_settings_btn)
        settings_layout.setSpacing(20)
        settings_layout.addWidget(self.other_settings_btn)
        settings_layout.setSpacing(20)
        settings_layout.addStretch(1)
        layout.addLayout(settings_layout)
        layout.addStretch(1)
        self.setLayout(layout)
    

        
        
        
        
            
            
    