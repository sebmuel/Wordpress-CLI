import typer
import os
from classes.CoreController import CoreController
from classes.Config import WpConfig


class WpApp:

    cli = typer.Typer()
    core = CoreController()
    config = WpConfig()

    def run(self):
        WpApp.cli()

    @staticmethod
    def verify_folders(specifc: str = None):
        if specifc != None:
            return os.path.exists(specifc)
        # TODO loop over every folder to check if exists

    @staticmethod
    @cli.command()
    def update():
        WpApp.core.version_controller.update()

    @staticmethod
    @cli.command()
    def get_latest():
        root = WpApp.config.cnf["root"]
        WpApp.core.version_controller.get_latest(root)
        
    @staticmethod
    @cli.command()
    def show_latest_zip():
        WpApp.core.version_controller.get_current_zip_version()
