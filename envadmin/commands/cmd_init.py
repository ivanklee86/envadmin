import os
from pathlib import Path
from configparser import ConfigParser
import click
from cryptography.fernet import Fernet
from git.repo import Repo
from gitsecret import GitSecret
from tinydb import TinyDB
from envadmin.cli import pass_context, Context


@click.command()
@click.option('-p', '--path', required=True, type=click.Path(), help="git repo to store environment variables.")
@click.option('-c', '--config-path', default=str(Path.home()), type=click.Path(), help="Folder to create .envadmin file.")
@click.option('-e', '--gpg-email', default=None, type=str, help="E-mail of gpg key to use for encrypting git repo.")
@click.option('--push/--no-push', default=True, help="Don't persist changes to remote git.")
@pass_context
def cli(ctx: Context, path: str, config_path: str, gpg_email: str, push: bool) -> None:
    """Initializes envadmin git repository."""
    if not os.path.isdir(path):
        raise click.ClickException("envadmin - Path isn't a directory.  Check the '-p/--path' option.")

    # Create .envadmin if available.
    if not os.path.isfile(os.path.join(config_path, ".envadmin")):
        config = ConfigParser()
        config.add_section("main")
        config.set("main", "repo_path", str(path))

        with open(os.path.join(config_path, ".envadmin"), "w") as config_file:
            config.write(config_file)

        ctx.vlog("Created .envadmin file in %s" % config_path)

    # Initialize gitsecret.
    gitsecret_repo = GitSecret(path=path)
    gitsecret_repo.create()
    gitsecret_repo.tell(gpg_email)
    ctx.vlog("Initialized git secret and added gpg signing key.")

    # Generate Fernet key and save to repo
    key = Fernet.generate_key()

    with open(os.path.join(path, "key.txt"), "w") as key_file:
        key_file.write(key.decode("UTF-8"))

    gitsecret_repo.add(os.path.join(path, "key.txt"), autoadd=True)
    gitsecret_repo.hide(clean_unencrypted=True)

    ctx.vlog("Generated encryption key.")

    # Initialize database
    TinyDB(os.path.join(path, 'envadmin.json'))
    ctx.vlog("envadmin database created.")

    # Commit and push to origin (if it exists).
    repo = Repo(path=path)
    repo.config_writer().set_value("user", "name", "envadmin").release()
    repo.config_writer().set_value("user", "email", "envadmin@envadmin.com").release()
    repo.git.add(".")
    repo.git.commit("-m", "Initial repo creation.")
    ctx.vlog("All files commited to git repo.")

    if [x for x in repo.remotes if x.name == "origin"] and push:
        repo.git.push('origin', 'master')
        ctx.vlog("Changes pushed to origin.")
