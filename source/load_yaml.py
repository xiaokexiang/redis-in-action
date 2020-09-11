import os

import yaml


def get(filename):
    yaml_path = os.path.join(os.path.dirname(__file__), filename)
    return yaml.load(open(yaml_path, 'r', encoding='utf-8').read(), Loader=yaml.FullLoader)
