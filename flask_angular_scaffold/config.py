import os
from ConfigParser import ConfigParser, NoOptionError

def get_config(config_location = "~/flask_angular_scaffold.ini"):
    try:
        config = ConfigParser()
        config.read(os.path.expanduser(config_location))
        return config
    except Exception as e:
        print "Could not load config file : " + str(e)

if __name__ == "__main__":
    config = get_config()

    print config
