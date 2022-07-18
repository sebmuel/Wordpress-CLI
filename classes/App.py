import typer
import os
from classes.CoreController import CoreController


class WpApp:

    cli = typer.Typer()
    core = CoreController()

    @staticmethod
    def run(action):
        WpApp.cli()
        action()

    @staticmethod
    def verify_folders(specifc: str = None):
        if specifc != None:
            return os.path.exists(specifc)
        # TODO loop over every folder to check if exists

    @staticmethod
    @cli.command()
    def update():
        WpApp.core.version_controller.run_command(function="update")

    @staticmethod
    @cli.command()
    def update2():
        pass
