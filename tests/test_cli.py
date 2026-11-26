"""Tests for CLI skeleton."""

from typer.testing import CliRunner

from cybershield import __version__
from cybershield.cli import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Beginner-friendly defensive cybersecurity toolkit" in result.output


def test_cli_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"CyberShield-Toolkit v{__version__}" in result.output


def test_subcommand_helps():
    subcommands = ["password", "caesar", "integrity", "phishing", "iplookup", "auth"]
    for cmd in subcommands:
        result = runner.invoke(app, [cmd, "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output


def test_password_cli():
    result = runner.invoke(app, ["password", "P@ssw0rd123!Secure"])
    assert result.exit_code == 0
    assert "Score:" in result.output
    assert "Strength:" in result.output
    assert (
        "P@ssw0rd123!Secure" not in result.output
    )  # Ensure password is not echoed back
