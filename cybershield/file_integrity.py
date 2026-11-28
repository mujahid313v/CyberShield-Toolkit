"""File integrity checker module using SHA-256 hashes."""

import hashlib
import json
from pathlib import Path
from typing import Any

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "build",
    "dist",
}


def hash_file(file_path: Path, chunk_size: int = 65536) -> str:
    """Compute SHA-256 hash of a file in memory-efficient chunks."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except (PermissionError, OSError):
        raise


def scan_path(
    target_path: Path, baseline_file: Path | None = None
) -> dict[str, dict[str, Any]]:
    """Scan file or directory recursively and return relative path to metadata mapping."""
    target_path = target_path.resolve()
    results = {}

    if target_path.is_file():
        try:
            file_hash = hash_file(target_path)
            stat = target_path.stat()
            results[target_path.name] = {
                "hash": file_hash,
                "size": stat.st_size,
            }
        except (PermissionError, OSError):
            pass
        return results

    if not target_path.is_dir():
        raise FileNotFoundError(f"Path not found or unreadable: {target_path}")

    baseline_resolved = baseline_file.resolve() if baseline_file else None

    for path in target_path.rglob("*"):
        # Check exclusion directories
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue

        # Skip symlinks escaping target folder or pointing outside
        if path.is_symlink():
            resolved = path.resolve()
            try:
                resolved.relative_to(target_path)
            except ValueError:
                continue

        if path.is_file():
            # Do not hash the baseline file itself
            if baseline_resolved and path.resolve() == baseline_resolved:
                continue

            try:
                rel_path = str(path.relative_to(target_path).as_posix())
                file_hash = hash_file(path)
                stat = path.stat()
                results[rel_path] = {
                    "hash": file_hash,
                    "size": stat.st_size,
                }
            except (PermissionError, OSError):
                continue

    return results


def save_baseline(target_path: Path, output_file: Path) -> dict[str, Any]:
    """Generate and save baseline JSON for file integrity."""
    data = scan_path(target_path, baseline_file=output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    return data


def verify_baseline(target_path: Path, baseline_file: Path) -> dict[str, Any]:
    """Verify current files against a saved baseline JSON."""
    if not baseline_file.exists():
        raise FileNotFoundError(f"Baseline file not found: {baseline_file}")

    with open(baseline_file, encoding="utf-8") as f:
        baseline_data: dict[str, dict[str, Any]] = json.load(f)

    current_data = scan_path(target_path, baseline_file=baseline_file)

    baseline_keys = set(baseline_data.keys())
    current_keys = set(current_data.keys())

    modified = []
    new_files = sorted(list(current_keys - baseline_keys))
    deleted_files = sorted(list(baseline_keys - current_keys))

    common = baseline_keys & current_keys
    for key in sorted(common):
        if baseline_data[key]["hash"] != current_data[key]["hash"]:
            modified.append(key)

    is_ok = not (modified or new_files or deleted_files)

    return {
        "ok": is_ok,
        "modified": modified,
        "new": new_files,
        "deleted": deleted_files,
        "total_baseline": len(baseline_keys),
        "total_current": len(current_keys),
    }
