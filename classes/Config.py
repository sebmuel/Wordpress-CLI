import json
import os


class WpConfig:

    def __init__(self) -> None:
        with open(os.path.dirname(os.path.abspath("config.json")) + "/config.json") as cnf:
            self.cnf = json.load(cnf)
