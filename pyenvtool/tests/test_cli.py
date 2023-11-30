"""Test `pyenvtool` package CLI tests."""
from click.testing import CliRunner

from pyenvtool.__main__ import cli_main


def test_cli_click() -> None:
    """Test the Click CLI."""
    runner = CliRunner()
    result = runner.invoke(cli_main)

    assert result.exit_code == 0

    help_result = runner.invoke(cli_main, ["--help"])

    assert help_result.exit_code == 0
    assert "--help" in help_result.output
    assert "Show this message and exit." in help_result.output
