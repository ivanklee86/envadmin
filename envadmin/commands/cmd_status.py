import os
import configparser
from pathlib import Path
from git.repo import Repo
from git.exc import GitError
import click
from envadmin import constants


@click.command()
@click.option('-c', '--config-path', default=str(Path.home()), type=click.Path(), help="Folder of .envadmin file.")
def cli(config_path: str) -> None:
    """Prints information about envadmin configuration."""
    click.echo("📝 Envadmin Status 📝")
    click.echo("Version: %s" % constants.VERSION)

    if os.path.isfile(os.path.join(config_path, ".envadmin")):
        click.echo("Configuration: Found")

        parser = configparser.ConfigParser()
        parser.read(os.path.join(config_path, ".envadmin"))
        repo_path = parser.get("main", "repo_path")
    else:
        click.echo("Configuration: Not found!")
        click.echo("Git Repo: N/A")
        return

    if os.path.isdir(repo_path):
        try:
            Repo(repo_path)
            click.echo("Git Repo: Found")
        except GitError:
            click.echo("Git Repo: Error loading git information.")
            return
    else:
        click.echo("Git Repo: Path not valid.")
        return
