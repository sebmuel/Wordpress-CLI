import typer
from os import path, makedirs, scandir
import requests, zipfile, io
from config import config

wp_cli = typer.Typer()


@wp_cli.command()
def wp_install():
    if is_installed():
        version_check(True)
        plugin_list()
        return

    makedirs(inst_path)
    latest = requests.get("https://wordpress.org/latest.zip")
    zip_file = zipfile.ZipFile(io.BytesIO(latest.content))
    zip_file.extractall("/home/sebastian/Backups/Wordpress/latest")
    typer.echo(f"Wordpress Version {version_check()} wurde erfolgreich intalliert")
 

@wp_cli.command()
def version_check(print=False):
    inst_path = config.get("install_path")
    with open(inst_path + "/wordpress/wp-includes/version.php", "r") as version:
        version = version.readlines()
        version = [x for x in version if "$wp_version" in x]
        version = version[1].split(" = ")
        version = str(version[1].strip().replace(";", ""))
    if print:
        typer.echo(f"Aktuell installierte Version Wordpress {version}")
    else:
        return version


def is_installed():
    if path.exists(inst_path):
        return True
    return False

@wp_cli.command()
def plugin_list(output=False):
    if is_installed:
        for dir in scandir(inst_path + "/wordpress/wp-content/plugins"):
            if dir.is_dir() and not output:
                typer.echo(dir)
            elif dir.is_dir() and output:
                p_list: list
                p_list += dir
                return p_list

            

if __name__ == '__main__':
    inst_path = config.get("install_path")
    root_path = config.get("root_path")
    wp_cli()