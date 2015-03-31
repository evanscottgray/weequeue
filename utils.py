import redis
import os.path
import ConfigParser

CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'config.ini'))


def parse_config():
    config_parser = ConfigParser.RawConfigParser()
    config_parser.read(CONFIG_FILE)
    config = {}
    for name, value in config_parser.items('weequeue'):
        if ',' in value:
            config[name] = value.split(',')
        else:
            config[name] = value
    return config


def get_redis_client(conf=parse_config()):
    r = redis.StrictRedis(host=conf['redis_host'],
                          password=conf['redis_pass'],
                          port=conf['redis_port'],
                          db=0)
    return r
