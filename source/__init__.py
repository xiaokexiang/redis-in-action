import logging

import redis

from source import load_yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
prop = load_yaml.get('../properties/env.yaml')
connection = redis.Redis(host=prop['redis']['server'],
                         port=prop['redis']['port'],
                         db=prop['redis']['db'],
                         password=prop['redis']['password'])
