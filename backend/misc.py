import configparser
from os import path


DIR_PATH = path.abspath(path.dirname(__file__))
CONFIG_FILE_NAME = "conf.ini"
FULL_CONFIG_FILE_PATH = f"{DIR_PATH}{path.sep}{CONFIG_FILE_NAME}"

def checkConfigFile():
    '''Check ConfigFile integrity'''
    if not path.exists(FULL_CONFIG_FILE_PATH):
        raise FileNotFoundError(f"File {FULL_CONFIG_FILE_PATH} not found")


def checkDBVars(db_vars:configparser.SectionProxy):
    ''' Check db Vars '''
    required_keys = ["hostname", "port", "username", "password"]
    if not all(db_vars.get(key, fallback=None) for key in required_keys):
        raise AttributeError(f"Some of the DB Vars are not in the {FULL_CONFIG_FILE_PATH} file.")

 
def loadAndReadDBConfig():
    checkConfigFile()
    config = configparser.ConfigParser()
    config.read(FULL_CONFIG_FILE_PATH)
    db_vars = config["DATABASE"]
    checkDBVars(db_vars)
    return db_vars
    

loadAndReadDBConfig()