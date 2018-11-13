import os
from envadmin.cli import cli
from tests.utilities.fixtures import runner, temp_folder, temp_git_folder  # noqa: F401


def test_e2e_init(runner, temp_git_folder):  # noqa: F811
    result = runner.invoke(cli, ["-v", "init",
                                 "-p", temp_git_folder,
                                 "-c", temp_git_folder,
                                 "-e", "test@test.com",
                                 "--no-push"])

    assert result.exit_code == 0
    assert os.path.isdir(os.path.join(temp_git_folder, ".gitsecret"))
    assert not os.path.isfile(os.path.join(temp_git_folder, "key.txt"))
    assert os.path.isfile(os.path.join(temp_git_folder, "key.txt.secret"))
    assert os.path.isfile(os.path.join(temp_git_folder, "envadmin.json"))
