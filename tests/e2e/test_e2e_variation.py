from click.testing import CliRunner
from envadmin.cli import cli
from tests.utilities import constants
from tests.utilities.fixtures import runner, temp_folder, temp_git_folder, temp_envadmin_folder  # noqa: F401


def test_e2e_variation_create(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    result = runner.invoke(cli, ["variation",
                                 "-c", temp_git_folder,
                                 "-n", constants.NAMESPACE1,
                                 "create",
                                 "-v", constants.VARIATION_1_1])

    print(result.output)
    assert result.exit_code == 0

    result = runner.invoke(cli, ["variation",
                                 "-c", temp_git_folder,
                                 "-n", constants.NAMESPACE1,
                                 "list"])

    assert constants.VARIATION_1_1 in result.output
    assert result.exit_code == 0


def test_e2e_variation_create_duplicate(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    runner.invoke(cli, ["variation",
                        "-c", temp_git_folder,
                        "-n", constants.NAMESPACE1,
                        "create",
                        "-v", constants.VARIATION_1_1])

    runner.invoke(cli, ["variation",
                        "-c", temp_git_folder,
                        "-n", constants.NAMESPACE1,
                        "create",
                        "-v", constants.VARIATION_1_2])

    result = runner.invoke(cli, ["variation",
                                 "-c", temp_git_folder,
                                 "-n", constants.NAMESPACE1,
                                 "list"])

    assert constants.VARIATION_1_1 in result.output
    assert constants.VARIATION_1_2 in result.output
    assert result.exit_code != 0


def test_e2e_variation_create_duplicate(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    result = runner.invoke(cli, ["variation",
                                 "-c", temp_git_folder,
                                 "-n", constants.NAMESPACE1,
                                 "create",
                                 "-v", constants.VARIATION_1_1])

    print(result.output)
    assert result.exit_code == 0

    result = runner.invoke(cli, ["variation",
                                 "-c", temp_git_folder,
                                 "-n", constants.NAMESPACE1,
                                 "create",
                                 "-v", constants.VARIATION_1_1])

    assert "Error: Namespace already presen" in result.output
    assert result.exit_code != 0


def test_e2e_namespace_delete_success(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    runner.invoke(cli, ["variation",
                        "-c", temp_git_folder,
                        "-n", constants.NAMESPACE1,
                        "create",
                        "-v", constants.VARIATION_1_1])

    runner.invoke(cli, ["variation",
                        "-c", temp_git_folder,
                        "-n", constants.NAMESPACE1,
                        "delete",
                        "-v", constants.VARIATION_1_1],
                  input="y")

    result = runner.invoke(cli, ["variation",
                                 "-c", temp_git_folder,
                                 "-n", constants.NAMESPACE1,
                                 "list"])
    assert result.exit_code == 0
    assert constants.VARIATION_1_1 not in result.output


def test_e2e_namespace_delete_default(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    result = runner.invoke(cli, ["variation",
                                 "-c", temp_git_folder,
                                 "-n", constants.NAMESPACE1,
                                 "delete",
                                 "-v", "__default"],
                           input="y")

    assert result.exit_code == 0
    assert "Cannot delete namespace defaults." in result.output
