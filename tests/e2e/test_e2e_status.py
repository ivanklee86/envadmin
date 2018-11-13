from click.testing import CliRunner
from envadmin.cli import cli
from tests.utilities.fixtures import runner, temp_folder, temp_git_folder, temp_envadmin_folder  # noqa: F401


def test_e2e_status(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    result = runner.invoke(cli, ["status",
                                 "-c", temp_git_folder])

    assert result.exit_code == 0
    assert "Version:" in result.output
    print(result.output)


def test_e2e_status_bad_config(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    result = runner.invoke(cli, ["status",
                                 "-c", "wat/is/this/even"])

    assert result.exit_code == 0
    assert "Version:" in result.output
    print(result.output)


def test_e2e_status_bad_git_repo(runner, temp_folder):  # noqa: F811
    runner = CliRunner()
    result = runner.invoke(cli, ["-v",
                                 "status",
                                 "-c", temp_folder])

    assert result.exit_code == 0
    assert "Version:" in result.output
    print(result.output)
