from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

class LineEditSettingsItem(QWidget):
    """
    Settings Item
    """

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.value = None
        
        self.lbl_name = QLabel(name + ":")
        self.lbl_name.setStyleSheet("font-weight: bold;")
        self.lbl_name.setFixedWidth(100)
        self.lbl_value = QLineEdit()
        self.lbl_value.setStyleSheet("background-color: #f0f0f0;")
        self.lbl_value.setFixedWidth(200)

        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self.lbl_name)
        layout.addSpacing(5)
        layout.addWidget(self.lbl_value)
        layout.addStretch(1)
        self.setLayout(layout)
    
    def set_value(self, value):
        self.lbl_value.setText(value)
        
    def get_value(self):
        return self.lbl_value.text()


class NTRIPSettingsPanelView(QWidget):
    """
    NTRIP Settings Panel View
    """

    def __init__(
        self,
        config,
    ):
        super().__init__()
        
        self._config = config
        
        self.ntrip_username_le = LineEditSettingsItem("Username")
        self.ntrip_password_le = LineEditSettingsItem("Password")
        self.ntrip_password_le.lbl_value.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(
            "font-weight: bold; font-size: 16px; background-color: #4CAF50; color: white;"
        )
        self.save_btn.setFixedWidth(100)
        self.save_btn.setFixedHeight(50)
        
        self.sync_btn = QPushButton("Sync")
        self.sync_btn.setStyleSheet(
            "font-weight: bold; font-size: 16px; background-color: #2196F3; color: white;"
        )
        self.sync_btn.setFixedWidth(100)
        self.sync_btn.setFixedHeight(50)
        
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.ntrip_username_le)
        layout.addWidget(self.ntrip_password_le)
        layout.addSpacing(10)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.sync_btn)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addStretch(1)
        layout.addLayout(btn_layout)
        layout.addStretch(1)
        self.setLayout(layout)
        
    def set_ntrip_params(self, params):
        if "username" in params:
            self.ntrip_username_le.set_value(params["username"])
        if "password" in params:
            self.ntrip_password_le.set_value(params["password"])
        
    def get_ntrip_params(self):
        
        params = {
            "username": self.ntrip_username_le.get_value(),
            "password": self.ntrip_password_le.get_value(),
        }
        
        # check if any of the values are empty
        for key, value in params.items():
            if not value:
                # prompt the user to fill in the missing value
                QMessageBox.warning(
                    self,
                    "Missing Value",
                    f"Please fill in the {key} field.",
                )
                return None
            
        return params