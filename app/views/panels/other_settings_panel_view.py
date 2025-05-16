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

class SettingsItem(QWidget):
    def __init__(self):
        super().__init__()
    
    def get_value(self) -> float:
        """Get the current value of the settings item."""
        raise NotImplementedError("Subclasses should implement this method.")

    def set_value(self, value: float) -> None:
        """Set the value of the settings item."""
        raise NotImplementedError("Subclasses should implement this method.")

class SettingSliderItem(SettingsItem):
    def __init__(
        self,
        label: str,
        min: float = 0,
        max: float = 100,
        step: float = 1,
        fixed_width: int = 200,
    ): 
        super().__init__()
        
        self.label_text = label
        self.min = min
        self.max = max
        self.step = step
        
        # Calculate scale factor once during initialization
        self.scale_factor = int(1 / self.step)
        
        self.label = QLabel(f"{self.label_text}: {min:.2f}")
        self.label.setFixedWidth(fixed_width)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFixedWidth(250)
        self.slider.setMinimum(int(self.min * self.scale_factor))
        self.slider.setMaximum(int(self.max * self.scale_factor))
        self.slider.setSingleStep(1)  # Use integer steps internally
        self.slider.valueChanged.connect(self.update_label)
        
        # Apply styles
        self._apply_styles()
        self._init_ui()

    def _apply_styles(self):
        """Apply styles to slider - extracted for clarity"""
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 20px;
                background: #d3d3d3;
                border-radius: 10px;
            }
            QSlider::handle:horizontal {
                width: 20px;
                height: 40px;
                background: #5c5c5c;
                border: 1px solid #3c3c3c;
                border-radius: 10px;
                margin: -10px 0;
            }
        """)

    def _init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addSpacing(10)
        layout.addWidget(self.slider)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)  # Reduce wasted space
        self.setLayout(layout)
    
    def update_label(self, value):
        """Update the label with the current slider value."""
        scaled_value = value / self.scale_factor
        self.label.setText(f"{self.label_text}: {scaled_value:.2f}")
        
    def get_value(self) -> float:
        """Get the current value of the slider."""
        return self.slider.value() / self.scale_factor
    
    def set_value(self, value: float) -> None:
        """Set the slider to a specific value."""
        clamped_value = min(max(value, self.min), self.max)
        self.slider.setValue(int(clamped_value * self.scale_factor))
        
        
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
        
        self.settings_tab.addTab(self.control_tab, "Control")
        
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
        return self.control_tab.get_settings()
    
    def set_settings(self, settings: Dict[str, float]) -> None:
        """Set the values of the settings items."""
        self.control_tab.set_settings(settings)