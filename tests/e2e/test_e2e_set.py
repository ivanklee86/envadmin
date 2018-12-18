from click.testing import CliRunner
from envadmin.cli import cli
from tests.utilities import constants
from tests.utilities.fixtures import runner, temp_folder, temp_git_folder, temp_envadmin_folder  # noqa: F401


def test_e2e_set_create(runner, temp_git_folder, temp_envadmin_folder):  # noqa: F811
    runner = CliRunner()
    result = runner.invoke(cli, ["set",
                                 "-c", temp_git_folder,
                                 "-n", constants.NAMESPACE2,
                                 "-v", constants.VARIATION_2_1,
                                 "fur",
                                 "black"])

    runner.invoke(cli, ["set",
                        "-c", temp_git_folder,
                        "-n", constants.NAMESPACE2,
                        "-v", constants.VARIATION_2_1,
                        "tail",
                        "long"])

    print(result.output)
    assert result.exit_code == 0
