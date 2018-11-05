from click.testing import CliRunner
from envadmin.cli import cli


def test_e2e_status():
    runner = CliRunner()
    result = runner.invoke(cli, ["status"])

    assert result.exit_code == 0
    assert result.output == "Hello!\n"


def test_e2e_status_with_args():
    runner = CliRunner()
    result = runner.invoke(cli, ["-v", "status"])

    print(result.output)
    assert result.exit_code == 0
    assert result.output == "Hello!\nHello this is envadmin!\n"
