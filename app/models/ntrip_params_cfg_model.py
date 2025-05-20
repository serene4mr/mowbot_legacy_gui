import os
import yaml
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from typing import Dict, Any

from app.utils.logger import logger

class NTRIPParamsCfgModel(QObject):
    
    signal_settings_ntrip_synced = pyqtSignal(dict)
    
    _instance = None

    @staticmethod
    def get_instance(config: Dict[str, Any]) -> "NTRIPParamsCfgModel":
        """
        Returns the singleton instance of NTRIPParamsCfgModel.
        """
        if NTRIPParamsCfgModel._instance is None:
            NTRIPParamsCfgModel._instance = NTRIPParamsCfgModel(config)
        return NTRIPParamsCfgModel._instance

    def __init__(
        self,
        config,
    ):
        super().__init__()
        self._config = config
        self._ntrip_params_file = \
            self._config["mowbot_legacy_data_path"] \
            + "/" + self._config["ntrip_params_file"]
        
        self._ntrip_params = {}
        
    def set_params(self,params):
        
        for key, value in params.items():
            if key in self._ntrip_params:
                self._ntrip_params[key] = value
            else:
                logger.warning(f"Key {key} not found in NTRIP parameters.")
        
    def sync(self):
        
        if not os.path.exists(self._ntrip_params_file):
            logger.error(f"NTRIP params file not found: {self._ntrip_params_file}")
            return
        
        with open(self._ntrip_params_file, 'r') as file:
            self._ntrip_params = yaml.safe_load(file)["/**"]["ntrip_client"]["ros__parameters"]
        
        self.signal_settings_ntrip_synced.emit(self._ntrip_params)
            
        logger.info(f"NTRIP params loaded: {self._ntrip_params}")
            
    def apply(self):
        if not os.path.exists(self._ntrip_params_file):
            logger.error(f"NTRIP params file not found: {self._ntrip_params_file}")
            return
        
        with open(self._ntrip_params_file, 'w') as file:
            yaml.dump({"/**": {"ntrip_client": {"ros__parameters": self._ntrip_params}}}, file)
        
        logger.info(f"NTRIP params saved: {self._ntrip_params}")
        