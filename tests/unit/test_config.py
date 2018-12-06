from pathlib import Path
import pytest
from click import ClickException
from envadmin.utilities import config
from tests.utilities.fixtures import runner, temp_folder, temp_git_folder, temp_envadmin_folder  # noqa: F401


def test_config_parser(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    parser = config.get_config(Path(temp_git_folder))
    assert "envadmin_sandbox" in parser.get("main", "repo_path")


def test_config_parser_exception(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    with pytest.raises(ClickException) as excinfo:
        config.get_config("/what/ever")

        assert "Cannot find .envadmin file" in str(excinfo.value)
