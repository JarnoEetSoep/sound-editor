import json
import os

import Exceptions as e

class ConfigManager:
    """Class for managing your configuration files"""
    @staticmethod
    def create(path: str, initial: dict) -> 'ConfigManager':
        """Create a new configuration file"""
        try:
            open(path, 'r', encoding='UTF-8').close()
        except FileNotFoundError:
            with open(path, 'w', encoding='utf-8') as config:
                config.write(json.dumps(initial, indent=4))
                config.close()
            
            return ConfigManager.load(path, set(initial.keys()))
        else:
            raise e.ConfigurationAlreadyExists

    @staticmethod
    def load(path: str, keys: set) -> 'ConfigManager':
        """Load a configuration file"""
        try:
            config = open(path, 'r', encoding='UTF-8')
        except FileNotFoundError:
            raise e.ConfigurationDoesNotExist
        else:
            conf = json.loads(config.read())
            config.close()

            if type(conf) != dict:
                raise e.ConfigurationFileInvalid

            if set(conf.keys()).difference(keys) != set():
                raise e.TooManyKeysWereFoundException

            if keys.difference(conf.keys()) != set():
                raise e.TooFewKeysWereFoundException

            return ConfigManager(conf, path)
    
    def __init__(self, config: dict, path: str):
        """Do not use this function, instead load a configuration using either ConfigManager.create() or Configmanager.load()"""
        self.config = config
        self.path = path
    
    def getConfig(self) -> dict:
        """Get the configuration to read stuff from it"""
        return self.config
    
    def setConfig(self, config: dict) -> 'ConfigManager':
        """Set the configuration, e.g. after making some changes to the original one"""
        self.config = config
        return self
    
    def save(self) -> 'ConfigManager':
        """Save the configuration to its file"""
        with open(self.path, 'w', encoding='utf-8') as config:
            config.write(json.dumps(self.config, indent=4))
            config.close()
        
        return self
    
    def getLang(self) -> dict:
        """Returns the current language file's contents (JSON)"""
        with open(os.path.realpath(os.path.dirname(__file__) + '/../' + self.config['lang']), 'r', encoding='UTF-8') as lang:
            language = json.loads(lang.read())
            lang.close()
        
        return language