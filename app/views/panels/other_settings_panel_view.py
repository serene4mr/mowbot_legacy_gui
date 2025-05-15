from PyQt5.QtWidgets import (
    QWidget,
)



class OtherSettingsPanelView(QWidget):
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self._config = config
        
        
        
        self._init_ui()
        
    def _init_ui(self):
        pass