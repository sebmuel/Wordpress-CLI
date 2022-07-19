#!/home/sebastian/Skripts/wp-cli/.venv/bin/python3.9
import progressbar
import json
import typer
import os
import requests
import zipfile
import io
import urllib


app = typer.Typer()


def load_config():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    # TODO ERROR HANDLING
    with open(os.path.join(__location__, "config.json")) as conf:
        config = json.load(conf)
    return config


def parse_params(params: dict):
    outter_key = "&request[fields]"
    url = ""
    for param in params.items():
        key = param[0]
        value = param[1]
        url += outter_key + f"%5B{key}%5D={1 if value else 0}"
    return url


def verify_folder(path: str):
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(root_path + "deploy/"):
        os.mkdir(path)


def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


@app.command()
def pull_latest(force: bool = False):
    # TODO do a check if the an installed zip file exists
    if (
        os.path.exists(os.path.join(root_path, deploy_dir + ".installed.json"))
        and not force
    ):
        with open(os.path.join(root_path, deploy_dir + ".installed.json")) as data:
            current_data = json.load(data)
            current_version = get_latest_version_number()
            if current_version in current_data.get("installed"):
                typer.echo(f"version {current_version} is already installed")
                return
    # check if json file exists if not fetch them and store them
    if not os.path.exists(
        os.path.join(root_path, (deploy_dir + version_list))
    ) or not os.path.exists(os.path.join(root_path, deploy_dir + download_list)):
        typer.echo(
            f"could not find .version.json file path: {os.path.join(root_path, (deploy_dir + version_list))}"
        )
        update()
    latest_version_number = get_latest_version_number()
    with open(os.path.join(root_path, deploy_dir + download_list)) as dl_list:
        download_dict = json.load(dl_list)
        for version in download_dict["offers"]:
            if (
                latest_version_number in version["download"]
                and version["response"] == "upgrade"
            ):
                download_url = version["download"]
                break
        typer.echo(f"Downloading Wordpress Version {latest_version_number}")
        request = urllib.request.urlretrieve(
            download_url,
            f"{os.path.join(root_path, deploy_dir)}wordpress-{latest_version_number}.zip",
            show_progress,
        )
        typer.echo(f"finished...")
        installed_file = {"installed": get_latest_version_number()}
        with open(
            os.path.join(root_path, deploy_dir + ".installed.json"), "w"
        ) as insalled_json:
            json.dump(installed_file, insalled_json)


@app.command()
def get_latest_version_number():
    with open(os.path.join(root_path, deploy_dir + version_list)) as json_file:
        lines = json.load(json_file)
        print(lines)
        for key, value in lines.items():
            if value == "latest":
                return key


@app.command()
def update():
    version_endpoint = "http://api.wordpress.org/core/stable-check/1.0/"
    version_list_request = requests.get(version_endpoint)
    request_data = version_list_request.json()
    if version_list_request.status_code == 200:
        with open(os.path.join(root_path, deploy_dir + version_list), "w") as json_file:
            json.dump(request_data, json_file)
            typer.echo(f"updated version list from {version_endpoint}")

    download_endpoint = "https://api.wordpress.org/core/version-check/1.7/"
    download_list_request = requests.get(download_endpoint)
    request_data = download_list_request.json()
    if download_list_request.status_code == 200:
        with open(
            os.path.join(root_path, deploy_dir + download_list), "w"
        ) as json_file:
            json.dump(request_data, json_file)
            typer.echo(f"updated download list from {download_endpoint}")


@app.command()
def create_deploy(name: str, clean: bool = False):
    if name == deploy_prefix:
        typer.echo(f"The name: {name} is reserved for the deploy prefix!")
        rechoice_name = input(f"choose a differnt name ...: ")
        rechoice_name.replace(" ", "")
        create_deploy(rechoice_name)
        return
    # TODO check if verison exists
    deploy_uri = os.path.join(root_path, name)
    if os.path.exists(deploy_uri + deploy_prefix):
        typer.echo(f"Deploy with the name: '{name}' already exists")
        return
    os.mkdir(os.path.join(root_path, name + deploy_prefix))
    with zipfile.ZipFile(
        os.path.join(
            root_path, deploy_dir +
            f"wordpress-{get_latest_version_number()}.zip"
        ),
        "r",
    ) as zip_ref:
        zip_ref.extractall(os.path.join(root_path, name + deploy_prefix))
    typer.echo(
        f"Version: {get_latest_version_number()} has been installed -> {deploy_uri + deploy_prefix}"
    )
    # if clean is True clean default themes and plugins from


@app.command()
def download_plugin(plugin_name: str):
    endpoint = f"https://api.wordpress.org/plugins/info/1.1/?action=query_plugins&request[search]={plugin_name}"
    params = {
        # fields we want
        "name": True,
        "author": True,
        "slug": True,
        "downloadlink": True,
        # fields we dont want
        "rating": False,
        "ratings": False,
        "downloaded": False,
        "description": False,
        "active_installs": False,
        "short_description": False,
        "donate_link": False,
        "tags": False,
        "sections": False,
        "homepage": False,
        "last_updated": False,
        "compatibility": False,
        "tested": False,
        "requires": False,
        "versions": False,
        "support_threads": False,
        "support_threads_resolved": False,
    }

    endpoint = endpoint + parse_params(params)
    request = requests.get(endpoint)
    plugins = request.json().get("plugins")
    max_hits = 10
    matches = dict()

    typer.echo(f"Found {len(plugins)} Plugins with the name {plugin_name}")
    for i, plugin in enumerate(plugins):
        print(plugin, plugin_name)
        name = typer.style(plugin.get("name"),
                           fg=typer.colors.GREEN, bold=True)
        if i >= max_hits:
            typer.echo(f"HITS: {max_hits-9} - {max_hits}")
            input(f"Press any key to continue or STRG-C to stop")
            max_hits += max_hits
        typer.echo(
            f"{typer.style(str(i+1), fg=typer.colors.RED, bold=True)} - {name}")
        matches[i + 1] = plugin.get("name")
    print(matches)


@app.command()
def show_deploy(deploy_name: str = False, list_all: bool = False):
    if not deploy_name and not list_all:
        typer.echo(f"need a deploy name or --list-all param")
        return
    elif list_all:
        for directory in os.listdir(os.path.realpath(root_path)):
            if deploy_prefix not in directory:
                continue
            typer.echo(
                f"{directory.replace(deploy_prefix, '')} -> {os.path.realpath(root_path)}"
            )
        return
    if os.path.exists(os.path.join(root_path, deploy_name + deploy_prefix)):
        typer.echo(
            f"Deploy exists under -> {os.path.join(root_path, deploy_name)}")
    else:
        typer.echo(f"No deploy with {deploy_name} was found ...")


if __name__ == "__main__":
    pbar = None
    config = load_config()
    root_path = str(config.get("root"))
    deploy_dir = str(config.get("deploy_folder"))
    version_list = str(config.get("version_list"))
    download_list = str(config.get("download_list"))
    deploy_prefix = str(config.get("deploy_prefix"))
    # check if folders exists if not create them
    verify_folder(root_path)
    verify_folder(root_path + "deploy/")
    # run the typer app
    app()
