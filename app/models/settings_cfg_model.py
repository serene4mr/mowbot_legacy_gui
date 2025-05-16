from PyQt5.QtCore import QObject
from pathlib import Path
import yaml

class SettingsCfgModel(QObject):
    """
    Settings configuration model.
    """

    def __init__(self):
        pass
        
    def set_settings(self, settings: dict) -> None:
        """
        Set the settings.
        """
        raise NotImplementedError("Subclasses should implement this method.")
        
    def get_settings(self):
        """
        Get the settings.
        """
        raise NotImplementedError("Subclasses should implement this method.")


class OtherSettingsCfgModel(SettingsCfgModel):
    
    _instance = None
    
    @staticmethod
    def get_instance(config) -> "OtherSettingsCfgModel":
        """
        Returns the singleton instance of OtherSettingsCfgModel.
        """
        if OtherSettingsCfgModel._instance is None:
            OtherSettingsCfgModel._instance = OtherSettingsCfgModel(config)
        return OtherSettingsCfgModel._instance

    def __init__(
        self, 
        config
        ):
        super().__init__()
        
        self._config = config
        self.cfg_files = {
            "cmdvel_scaler_node": Path(self._config["mowbot_legacy_data_path"]) / self._config["cmdvel_scaler_params_file"],
        }
        self.cfg_settings ={}
            
        
    def get_settings(self) -> dict:
        
        # read the yaml files
        for key, file in self.cfg_files.items():
            if not file.exists():
                raise FileNotFoundError(f"File {file} does not exist.")
            
            with open(file, 'r') as f:
                self.cfg_settings[key] = yaml.safe_load(f)["/**"][key]["ros__parameters"]
                
        return self.cfg_settings
                
    
    def set_settings(self, settings: dict) -> None:
        pass
        