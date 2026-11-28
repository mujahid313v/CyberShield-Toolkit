"""CLI entry point for CyberShield-Toolkit."""

from pathlib import Path
from typing import Annotated

import typer

from cybershield import __version__
from cybershield.caesar import caesar_brute_force, caesar_decrypt, caesar_encrypt
from cybershield.file_integrity import save_baseline, verify_baseline
from cybershield.password_checker import check_password_strength

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
    text: Annotated[
        str | None,
        typer.Argument(
            help="Password to evaluate (optional, prompts securely if omitted)."
        ),
    ] = None,
) -> None:
    """Check the strength of a password."""
    if not text:
        text = typer.prompt("Enter password to evaluate", hide_input=True)

    result = check_password_strength(text)
    typer.echo("\n[Password Strength Analysis]")
    typer.echo(f"  Score:      {result['score']}/100")
    typer.echo(f"  Strength:   {result['strength']}")
    typer.echo("  Suggestions:")
    for suggestion in result["suggestions"]:
        typer.echo(f"    - {suggestion}")


@app.command()
def caesar(
    text: Annotated[str, typer.Argument(help="Text to process.")],
    shift: Annotated[
        int, typer.Option("--shift", "-s", help="Shift value (1-25).")
    ] = 3,
    decrypt: Annotated[
        bool, typer.Option("--decrypt", "-d", help="Decrypt mode.")
    ] = False,
    brute: Annotated[
        bool, typer.Option("--brute", "-b", help="Brute-force all shifts.")
    ] = False,
) -> None:
    """Encrypt, decrypt, or brute-force a Caesar cipher (Educational)."""
    typer.echo("[Notice] Caesar cipher is an educational tool for demonstration.")
    if brute:
        typer.echo(f"\n[Caesar Brute-Force Demo] Text: '{text}'\n")
        results = caesar_brute_force(text)
        for s, decoded in results.items():
            typer.echo(f"  Shift {s:2d}: {decoded}")
    elif decrypt:
        res = caesar_decrypt(text, shift)
        typer.echo(f"\n[Caesar Decryption] (shift={shift})")
        typer.echo(f"  Result: {res}")
    else:
        res = caesar_encrypt(text, shift)
        typer.echo(f"\n[Caesar Encryption] (shift={shift})")
        typer.echo(f"  Result: {res}")


@app.command()
def integrity(
    path: Annotated[str, typer.Argument(help="File or directory path.")],
    baseline: Annotated[
        str, typer.Option("--baseline", "-b", help="Baseline JSON file path.")
    ] = "baseline.json",
    verify: Annotated[
        bool, typer.Option("--verify", "-v", help="Verify against saved baseline.")
    ] = False,
) -> None:
    """Check file integrity via SHA-256 hashes (create or verify baseline)."""
    target_path = Path(path)
    baseline_path = Path(baseline)

    if not target_path.exists():
        typer.echo(f"[Error] Path not found: {target_path}", err=True)
        raise typer.Exit(code=1)

    if verify:
        typer.echo(
            f"[file-integrity] Verifying {target_path} against baseline {baseline_path}..."
        )
        try:
            res = verify_baseline(target_path, baseline_path)
            typer.echo("\n[Integrity Verification Results]")
            typer.echo(f"  Baseline files: {res['total_baseline']}")
            typer.echo(f"  Current files:  {res['total_current']}")
            typer.echo(f"  Modified:       {len(res['modified'])}")
            for f in res["modified"]:
                typer.echo(f"    - {f}")
            typer.echo(f"  New:            {len(res['new'])}")
            for f in res["new"]:
                typer.echo(f"    - {f}")
            typer.echo(f"  Deleted:        {len(res['deleted'])}")
            for f in res["deleted"]:
                typer.echo(f"    - {f}")

            if res["ok"]:
                typer.echo("\nStatus: OK — All files match baseline.")
                return
            else:
                typer.echo(
                    "\nStatus: WARNING — Integrity violations detected!", err=True
                )
                raise typer.Exit(code=1)
        except Exception as e:
            typer.echo(f"[Error] {e}", err=True)
            raise typer.Exit(code=1)
    else:
        typer.echo(
            f"[file-integrity] Generating baseline for {target_path} -> {baseline_path}..."
        )
        try:
            data = save_baseline(target_path, baseline_path)
            typer.echo(
                f"\nBaseline saved successfully to {baseline_path} ({len(data)} files recorded)."
            )
        except Exception as e:
            typer.echo(f"[Error] {e}", err=True)
            raise typer.Exit(code=1)


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
