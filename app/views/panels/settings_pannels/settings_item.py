from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QSlider,
    QLineEdit,
)

from PyQt5.QtCore import Qt

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
        

class SettingsLineEditItem(SettingsItem):
    def __init__(
        self, 
        label: str, 
        fixed_width: int = 200,
        is_password: bool = False,
    ):
        super().__init__()
        
        self.label_text = label
        self.label = QLabel(self.label_text)
        self.label.setFixedWidth(fixed_width)
        
        self.line_edit = QLineEdit()
        self.line_edit.setEchoMode(QLineEdit.Password if is_password else QLineEdit.Normal)
        self.line_edit.setFixedWidth(250)
        
        # Apply styles
        self._apply_styles()
        self._init_ui()
    
    def _apply_styles(self):
        """Apply styles to line edit - extracted for clarity"""
        self.line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #5c5c5c;
                border-radius: 5px;
                padding: 5px;
            }
        """)
    
    def _init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addSpacing(10)
        layout.addWidget(self.line_edit)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)  # Reduce wasted space
        self.setLayout(layout)
    
    def get_value(self) -> str:
        """Get the current value of the line edit."""
        return self.line_edit.text()
    
    def set_value(self, value: str) -> None:
        """Set the line edit to a specific value."""
        self.line_edit.setText(value)