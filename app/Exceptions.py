class ConfigurationDoesNotExist(Exception):
    """Raised when the requested configuration file does not exist"""
    pass

class ConfigurationFileInvalid(Exception):
    """Raised when the requested configuration file is not valid JSON"""
    pass

class TooFewKeysWereFoundException(Exception):
    """Raised when too few keys were found when loading a configuration file"""
    pass

class TooManyKeysWereFoundException(Exception):
    """Raised when too many keys were found when loading a configuration file"""
    pass

class ConfigurationAlreadyExists(Exception):
    """Raised when the configuration file that you want to create already exists"""
    pass

class SaveFileError(Exception):
    """Raised when the current file could not be saved"""
    pass