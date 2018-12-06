import os
import shutil
import uuid
from pathlib import Path
import pytest
from click.testing import CliRunner
from git.repo import Repo
from envadmin.cli import cli


PATH = os.path.join(Path.home(), "temp", "envadmin_sandbox", str(uuid.uuid4())[:8])


@pytest.fixture()
def runner():
    yield CliRunner()


@pytest.fixture()
def temp_folder():
    # Deletes and recreates PATH
    if os.path.isdir(PATH):
        shutil.rmtree(PATH)

    os.mkdir(PATH)

    yield PATH

    # Clear files at end.
    shutil.rmtree(PATH)


@pytest.fixture()
def temp_git_folder(temp_folder):
    repo = Repo.init(temp_folder)
    repo.create_remote(name="origin", url="git@gitlab.com:temp/sandbox.git")
    yield temp_folder


@pytest.fixture()
def temp_envadmin_folder(runner, temp_git_folder):
    runner.invoke(cli, ["-v", "init",
                        "-p", temp_git_folder,
                        "-c", temp_git_folder,
                        "-e", "test@test.com",
                        "--no-push"])

    runner.invoke(cli, ["namespace",
                        "-c", temp_git_folder,
                        "create",
                        "-n", "Namespace1"])
