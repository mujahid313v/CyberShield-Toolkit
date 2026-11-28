"""Tests for CLI skeleton."""

from pathlib import Path

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


def test_caesar_cli():
    result = runner.invoke(app, ["caesar", "abc", "--shift", "1"])
    assert result.exit_code == 0
    assert "bcd" in result.output

    result_dec = runner.invoke(app, ["caesar", "bcd", "--shift", "1", "--decrypt"])
    assert result_dec.exit_code == 0
    assert "abc" in result_dec.output

    result_brute = runner.invoke(app, ["caesar", "abc", "--brute"])
    assert result_brute.exit_code == 0
    assert "Shift" in result_brute.output


def test_integrity_cli(tmp_path: Path):
    d = tmp_path / "proj"
    d.mkdir()
    (d / "file.txt").write_text("hello", encoding="utf-8")
    baseline = tmp_path / "base.json"

    # Create baseline
    res = runner.invoke(app, ["integrity", str(d), "--baseline", str(baseline)])
    assert res.exit_code == 0
    assert "Baseline saved successfully" in res.output

    # Verify OK
    res_v = runner.invoke(
        app, ["integrity", str(d), "--baseline", str(baseline), "--verify"]
    )
    assert res_v.exit_code == 0
    assert "Status: OK" in res_v.output

    # Modify file -> verify fail (exit code 1)
    (d / "file.txt").write_text("modified", encoding="utf-8")
    res_m = runner.invoke(
        app, ["integrity", str(d), "--baseline", str(baseline), "--verify"]
    )
    assert res_m.exit_code == 1
    assert "WARNING" in res_m.output
