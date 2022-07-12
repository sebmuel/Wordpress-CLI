import json
import typer
import os

"""
functions to load the config
"""


def load_config():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, "config.json")) as conf:
        config = json.load(conf)
    return config


config = load_config()
print(config)
