from click.testing import CliRunner
from envadmin.cli import cli
from tests.utilities import constants
from tests.utilities.fixtures import runner, temp_folder, temp_git_folder, temp_envadmin_folder  # noqa: F401


def test_e2e_namespace_create(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    result = runner.invoke(cli, ["namespace",
                                 "-c", temp_git_folder,
                                 "create",
                                 "-n", constants.NAMESPACE2])

    assert result.exit_code == 0

    result = runner.invoke(cli, ["namespace",
                                 "-c", temp_git_folder,
                                 "list"])

    assert result.exit_code == 0
    assert constants.NAMESPACE2 in result.output


def test_e2e_namespace_delete_success(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    result = runner.invoke(cli, ["namespace",
                                 "-c", temp_git_folder,
                                 "delete",
                                 "-n", constants.NAMESPACE2],
                           input="y")

    assert result.exit_code == 0

    result = runner.invoke(cli, ["namespace",
                                 "-c", temp_git_folder,
                                 "list"])

    assert result.exit_code == 0
    assert constants.NAMESPACE2 not in result.output


def test_e2e_namespace_delete_failure(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    result = runner.invoke(cli, ["namespace",
                                 "-c", temp_git_folder,
                                 "delete",
                                 "-n", constants.NAMESPACE1],
                           input="n")

    assert result.exit_code == 0

    result = runner.invoke(cli, ["namespace",
                                 "-c", temp_git_folder,
                                 "list"])

    assert result.exit_code == 0
    assert constants.NAMESPACE1 in result.output
