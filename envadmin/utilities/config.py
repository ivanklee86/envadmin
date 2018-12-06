import os
import configparser
from pathlib import Path
from typing import Optional
import click


def get_config(config_path: Optional[Path]) -> configparser.ConfigParser:
    """Retrieves config object from .envadmin."""
    if config_path:
        target_path = config_path
    else:
        target_path = Path.home()

    dotfile_path = os.path.join(target_path, ".envadmin")

    if os.path.isfile(dotfile_path):
        parser = configparser.ConfigParser()
        parser.read(dotfile_path)
    else:
        raise click.ClickException("envadmin - Cannot find .envadmin file.")

    return parser
