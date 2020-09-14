import logging
import os

import redis
import yaml


def get(filename):
    yaml_path = os.path.join(os.path.dirname(__file__), filename)
    return yaml.load(open(yaml_path, 'r', encoding='utf-8').read(), Loader=yaml.FullLoader)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
prop = get('../properties/env.yaml')
connection = redis.Redis(host=prop['redis']['server'],
                         port=prop['redis']['port'],
                         db=prop['redis']['db'],
                         password=prop['redis']['password'])
