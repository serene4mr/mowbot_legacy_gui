from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTabWidget,
    QLabel,
    QSlider,
)

from PyQt5.QtCore import Qt, pyqtSignal

from typing import Dict

from .settings_item import (
    SettingsItem, 
    SettingSliderItem,
    SettingsLineEditItem,
)
        
class SettingsTabWidget(QWidget):
    def __init__(
        self,
        settings_items: Dict[str, SettingsItem],
    ):
        super().__init__()
        
        self.setting_items = settings_items
        
        self._init_ui()
        
    def _init_ui(self):
        layout = QVBoxLayout()
        
        for item in self.setting_items.values():
            layout.addSpacing(20)
            layout.addWidget(item)
            
        layout.addStretch(1)
        self.setLayout(layout)
    
    def get_settings(self) -> Dict[str, float]:
        """Get the current settings from all items."""
        settings = {}
        for name, item in self.setting_items.items():
            print(f"Getting value for {name}: {item.get_value()}")
            settings[name] = item.get_value()
        return settings
    
    def set_settings(self, settings: Dict[str, float]) -> None:
        """Set the values of the settings items."""
        for name, value in settings.items():
            if name in self.setting_items:
                item = self.setting_items[name]
                item.set_value(value)
        
    
class OtherSettingsPanelView(QWidget):
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self._config = config
        
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.setStyleSheet(
            "font-weight: bold; font-size: 16px; background-color: #4CAF50; color: white;"
        )
        self.apply_btn.setFixedWidth(100)
        self.apply_btn.setFixedHeight(50)
        
        self.sync_btn = QPushButton("Sync")
        self.sync_btn.setStyleSheet(
            "font-weight: bold; font-size: 16px; background-color: #2196F3; color: white;"
        )
        self.sync_btn.setFixedWidth(100)
        self.sync_btn.setFixedHeight(50)
        
        self.settings_tab = QTabWidget()
        # increase tab height and font size
        self.settings_tab.setStyleSheet(
            """
            QTabBar::tab {
                height: 50px;
                width: 250px;
                font-size: 14px;
                font-weight: bold;
            }
            """
        )
        
        self.control_tab = SettingsTabWidget({
            "cmdvel_scaler_node.left_rate": SettingSliderItem("Left Motor Rate", 0, 1.0, 0.01, 200),
            "cmdvel_scaler_node.right_rate": SettingSliderItem("Right Motor Rate", 0, 1.0, 0.01, 200),
        })
        
        self.ktserver_tab = SettingsTabWidget({
            "kt_server_client_node.robot_serial": SettingsLineEditItem("Robot Serial", 200),
            "kt_server_client_node.client_id": SettingsLineEditItem("Client ID", 200),
            "kt_server_client_node.client_secret": SettingsLineEditItem("Client Secret", 200, True),
            "kt_server_client_node.robot_status_report_hz": SettingSliderItem("Status Report Rate (Hz)", 0, 10, 1, 200),
        })
            
        
        self.settings_tab.addTab(self.control_tab, "Control")
        self.settings_tab.addTab(self.ktserver_tab, "KT Server")
        
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the user interface layout."""
        layout = QHBoxLayout()
        layout.addWidget(self.settings_tab)
        layout.addStretch(1)

        # Buttons layout
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.sync_btn)
        btn_layout.setSpacing(20)
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addStretch(1)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
    def get_settings(self) -> Dict[str, float]:
        """Get the current settings from all items."""
        return {
            **self.control_tab.get_settings(), 
            **self.ktserver_tab.get_settings()
        }
    
    def set_settings(self, settings: Dict[str, float]) -> None:
        """Set the values of the settings items."""
        self.control_tab.set_settings(settings)
        self.ktserver_tab.set_settings(settings)