import os
import yaml


class Config:
    def __init__(self, env):
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
            self.config = config[env]

    def get(self, key, default=None):
        return self.config.get(key, default)


def get_config():
    env = os.environ.get('ENV', 'development')
    # 在启动的时候输入export ENV=production/development决定环境，默认为development
    return Config(env)
