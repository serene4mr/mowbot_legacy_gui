from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from pathlib import Path
import yaml

from app.utils.logger import logger

class SettingsCfgModel(QObject):
    """
    Settings configuration model.
    """

    def __init__(self):
        super().__init__()
        
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


class NtripSettingsCfgModel(SettingsCfgModel):

    signal_settings_ntrip_synced = pyqtSignal(dict)
    
    _instance = None

    @staticmethod
    def get_instance(config) -> "NtripSettingsCfgModel":
        """
        Returns the singleton instance of NTRIPParamsCfgModel.
        """
        if NtripSettingsCfgModel._instance is None:
            NtripSettingsCfgModel._instance = NtripSettingsCfgModel(config)
        return NtripSettingsCfgModel._instance
    
    def __init__(
        self,
        config,
    ):
        super().__init__()
        self._config = config
        self._ntrip_params_file = \
            Path(self._config["mowbot_legacy_data_path"]) / self._config["ntrip_params_file"]
            
    
    def get_settings(self):
        """
        Get the settings.
        """
        if not self._ntrip_params_file.exists():
            logger.error(f"NTRIP params file not found: {self._ntrip_params_file}")
            return {}
        
        with open(self._ntrip_params_file, 'r') as file:
            ntrip_params = yaml.safe_load(file)["/**"]["ntrip_client"]["ros__parameters"]
        
        return ntrip_params
    
    def set_settings(self, settings: dict) -> None:
        """
        Set the settings.
        """
        if not self._ntrip_params_file.exists():
            logger.error(f"NTRIP params file not found: {self._ntrip_params_file}")
            return
        
        with open(self._ntrip_params_file, 'w') as file:
            yaml.dump({"/**": {"ntrip_client": {"ros__parameters": settings}}}, file)
        
        logger.info(f"NTRIP params saved: {settings}")
    
    def apply(self, settings: dict) -> None:
        """
        Apply the settings.
        """
        self.set_settings(settings)
        
    def sync(self) -> None:
        """
        Sync the settings.
        """
        settings = self.get_settings()
        self.signal_settings_ntrip_synced.emit(settings)
        


class OtherSettingsCfgModel(SettingsCfgModel):
    
    signal_settings_other_synced = pyqtSignal(dict)
    
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
            "kt_server_client_node": Path(self._config["mowbot_legacy_data_path"]) / self._config["kt_server_bridge_params_file"],
        }
            
        
    def get_settings(self) -> dict:
        cfg_settings = {}
        
        for key, file in self.cfg_files.items():
            if not file.exists():
                raise FileNotFoundError(f"File {file} does not exist.")
            
            with open(file, 'r') as f:
                temp = yaml.safe_load(f)["/**"][key]["ros__parameters"]
                for k, v in temp.items():
                    cfg_settings[key + "." + k] = v
                
        return cfg_settings
                
    
    def set_settings(self, settings: dict) -> None:
        for key, value in settings.items():
            k1 , k2 = key.split(".")
            if k1 in self.cfg_files:
                with open(self.cfg_files[k1], 'r') as f:
                    temp = yaml.safe_load(f)
                
                if k2 in temp["/**"][k1]["ros__parameters"]:
                    temp["/**"][k1]["ros__parameters"][k2] = value
                else:
                    raise KeyError(f"Key {k2} not found in {k1} parameters.")
                
                with open(self.cfg_files[k1], 'w') as f:
                    yaml.dump(temp, f)
                
        logger.info(f"Settings saved: {settings}")
    
    def sync(self) -> None:
        """
        Sync the settings.
        """
        cfg_settings = self.get_settings()
        self.signal_settings_other_synced.emit(cfg_settings)
        
    def apply(self, settings: dict) -> None:
        """
        Apply the settings.
        """
        self.set_settings(settings)
        
        
        