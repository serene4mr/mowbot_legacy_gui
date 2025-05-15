from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QLabel, QDialogButtonBox, QGroupBox
)
from PyQt5.QtCore import Qt
from typing import Dict, Any

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QWidget
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QPushButton, QWidget

from .other_settings_panel_view import OtherSettingsPanelView
from .nav_settings_panel_view import NavSettingsPanelView
from .ntrip_settings_panel_view import NTRIPSettingsPanelView


class BaseSettingsDialog(QDialog):
    def __init__(self, title, content_widget: QWidget, fixed_size=(400, 300), parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(*fixed_size)

        # Remove all system buttons, keep only the title bar
        # self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        # Big Exit button at the top right
        # self.exit_btn = QPushButton("Exit")
        # self.exit_btn.setStyleSheet("""
        #     QPushButton {
        #         font-size: 18px;
        #         font-weight: bold;
        #         background-color: #d9534f;
        #         color: white;
        #         border-radius: 8px;
        #         padding: 12px 32px;
        #     }
        #     QPushButton:hover {
        #         background-color: #c9302c;
        #     }
        # """)
        # self.exit_btn.setFixedHeight(48)
        # self.exit_btn.setFixedWidth(120)
        # self.exit_btn.clicked.connect(self.reject)

        # top_layout = QHBoxLayout()
        # top_layout.addStretch(1)
        # top_layout.addWidget(self.exit_btn)

        main_layout = QVBoxLayout()
        # main_layout.addLayout(top_layout)
        main_layout.addWidget(content_widget)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        
class NavSettingsDialog(BaseSettingsDialog):
    def __init__(self, config, parent=None):
        nav_panel = NavSettingsPanelView(config)
        super().__init__(
            "Navigation Settings", nav_panel, 
            fixed_size=(850, 500), parent=parent)
        self.nav_panel = nav_panel
        
class NtripSettingsDialog(BaseSettingsDialog):
    def __init__(self, config, parent=None):
        ntrip_panel = NTRIPSettingsPanelView(config)
        super().__init__(
            "NTRIP Settings", ntrip_panel, fixed_size=(400, 200), parent=parent)
        self.ntrip_panel = ntrip_panel
        
class OtherSettingsDialog(BaseSettingsDialog):
    def __init__(self, config, parent=None):
        other_panel = OtherSettingsPanelView(config)
        super().__init__(
            "Other Settings", other_panel, fixed_size=(400, 200), parent=parent)
        self.other_panel = other_panel

class SettingsPanelView(QWidget):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self._config = config
        self._init_buttons()
        self._init_ui()
        self._connect_signals()
        
        self.nav_settings_dlg = NavSettingsDialog(self._config, self)
        self.ntrip_settings_dlg = NtripSettingsDialog(self._config, self)
        self.other_settings_dlg = OtherSettingsDialog(self._config, self)

    def _init_buttons(self):
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
        layout = QHBoxLayout()
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(20)
        settings_layout.addWidget(self.nav_settings_btn)
        settings_layout.addWidget(self.ntrip_settings_btn)
        settings_layout.addWidget(self.other_settings_btn)
        settings_layout.addStretch(1)
        layout.addLayout(settings_layout)
        layout.addStretch(1)
        self.setLayout(layout)

    def _connect_signals(self):
        self.nav_settings_btn.clicked.connect(self._show_nav_settings)
        self.ntrip_settings_btn.clicked.connect(self._show_ntrip_settings)
        self.other_settings_btn.clicked.connect(self._show_other_settings)

    def _show_nav_settings(self):
        self.nav_settings_dlg.exec_()

    def _show_ntrip_settings(self):
        self.ntrip_settings_dlg.exec_()

    def _show_other_settings(self):
        self.other_settings_dlg.exec_()
