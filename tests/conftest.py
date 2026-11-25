"""Shared test fixtures for CyberShield-Toolkit."""

import pytest
from typer.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture providing a Typer CLI test runner."""
    return CliRunner()
