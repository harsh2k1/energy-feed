import configparser

config_obj = configparser.ConfigParser()
config_obj.read('config/application-dev.ini')

config = {}
for section in config_obj.sections():
    inner_config = {}
    for key, value in config_obj[section].items():
        inner_config[key] = value
    
    config[section] = inner_config