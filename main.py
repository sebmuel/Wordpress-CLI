from rich.progress import Progress, SpinnerColumn, TextColumn
import json
from logging import root
import typer
import wget

app = typer.Typer()


def load_config():
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    # TODO ERROR HANDLING
    with open(os.path.join(__location__, "config.json")) as conf:
        config = json.load(conf)
    return config


def verify_deploy_folder():
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    if not os.path.exists(root_path + "deploy/"):
        os.mkdir(root_path + "deploy/")


@app.command()
def pull_latest():
    pass


@app.command()
def create_deploy():
    pass


if __name__ == "__main__":
    app()
    config = load_config()
    root_path = str(config.get("root"))
    verify_deploy_folder()
