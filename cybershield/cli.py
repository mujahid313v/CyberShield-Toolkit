"""CLI entry point for CyberShield-Toolkit."""

from typing import Annotated

import typer

from cybershield import __version__

app = typer.Typer(
    name="cybershield",
    help="Beginner-friendly defensive cybersecurity toolkit.",
    no_args_is_help=True,
)

auth_app = typer.Typer(help="Authentication & 2FA commands.")
app.add_typer(auth_app, name="auth")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"CyberShield-Toolkit v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option("--version", "-v", callback=_version_callback, is_eager=True),
    ] = None,
) -> None:
    """CyberShield-Toolkit: defensive cybersecurity CLI."""


@app.command()
def password(
    text: Annotated[str, typer.Argument(help="Password to evaluate.")],
) -> None:
    """Check the strength of a password."""
    typer.echo(f"[password-checker] Checking: {text}")


@app.command()
def caesar(
    text: Annotated[str, typer.Argument(help="Text to process.")],
    shift: Annotated[int, typer.Option(help="Shift value (1-25).")] = 3,
    decrypt: Annotated[
        bool, typer.Option("--decrypt", "-d", help="Decrypt mode.")
    ] = False,
    brute: Annotated[
        bool, typer.Option("--brute", "-b", help="Brute-force all shifts.")
    ] = False,
) -> None:
    """Encrypt, decrypt, or brute-force a Caesar cipher."""
    mode = "brute-force" if brute else ("decrypt" if decrypt else "encrypt")
    typer.echo(f"[caesar] {mode}: {text} (shift={shift})")


@app.command()
def integrity(
    path: Annotated[str, typer.Argument(help="File or directory path.")],
    verify: Annotated[
        bool, typer.Option("--verify", help="Verify against saved baseline.")
    ] = False,
) -> None:
    """Check file integrity via SHA-256 hashes."""
    action = "Verifying" if verify else "Hashing"
    typer.echo(f"[file-integrity] {action}: {path}")


@app.command()
def phishing(
    url: Annotated[str, typer.Argument(help="URL to analyse.")],
) -> None:
    """Detect phishing indicators in a URL."""
    typer.echo(f"[phishing-detector] Analysing: {url}")


@app.command()
def iplookup(
    ip: Annotated[str, typer.Argument(help="IP address to look up.")],
) -> None:
    """Look up geolocation info for an IP address."""
    typer.echo(f"[ip-lookup] Looking up: {ip}")


@auth_app.command("register")
def auth_register(
    username: Annotated[str, typer.Argument(help="Username to register.")],
) -> None:
    """Register a new user account."""
    typer.echo(f"[auth] Registering: {username}")


@auth_app.command("login")
def auth_login(
    username: Annotated[str, typer.Argument(help="Username to log in.")],
) -> None:
    """Log in to an existing account."""
    typer.echo(f"[auth] Logging in: {username}")


@auth_app.command("otp-setup")
def auth_otp_setup() -> None:
    """Generate a new TOTP secret for 2FA."""
    typer.echo("[auth] Generating OTP secret...")


@auth_app.command("otp-verify")
def auth_otp_verify(
    code: Annotated[str, typer.Argument(help="6-digit TOTP code.")],
) -> None:
    """Verify a TOTP code."""
    typer.echo(f"[auth] Verifying OTP: {code}")


if __name__ == "__main__":
    app()
