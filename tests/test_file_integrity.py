"""Tests for file integrity checker module."""

from pathlib import Path

import pytest

from cybershield.file_integrity import (
    hash_file,
    save_baseline,
    scan_path,
    verify_baseline,
)


def test_hash_file(tmp_path: Path):
    f = tmp_path / "test.txt"
    f.write_text("hello integrity", encoding="utf-8")
    h = hash_file(f)
    assert isinstance(h, str)
    assert len(h) == 64


def test_scan_single_file(tmp_path: Path):
    f = tmp_path / "single.txt"
    f.write_text("content", encoding="utf-8")
    res = scan_path(f)
    assert "single.txt" in res
    assert "hash" in res["single.txt"]
    assert res["single.txt"]["size"] == 7


def test_scan_missing_path():
    with pytest.raises(FileNotFoundError):
        scan_path(Path("nonexistent_path_12345"))


def test_baseline_save_and_verify_ok(tmp_path: Path):
    d = tmp_path / "project"
    d.mkdir()
    f1 = d / "a.txt"
    f1.write_text("file a", encoding="utf-8")
    f2 = d / "b.txt"
    f2.write_text("file b", encoding="utf-8")

    baseline_json = tmp_path / "baseline.json"
    data = save_baseline(d, baseline_json)
    assert len(data) == 2

    res = verify_baseline(d, baseline_json)
    assert res["ok"] is True
    assert len(res["modified"]) == 0
    assert len(res["new"]) == 0
    assert len(res["deleted"]) == 0


def test_baseline_verify_violations(tmp_path: Path):
    d = tmp_path / "project"
    d.mkdir()
    f1 = d / "a.txt"
    f1.write_text("file a", encoding="utf-8")
    f2 = d / "b.txt"
    f2.write_text("file b", encoding="utf-8")

    baseline_json = tmp_path / "baseline.json"
    save_baseline(d, baseline_json)

    # 1. Modify f1
    f1.write_text("modified content", encoding="utf-8")

    # 2. Delete f2
    f2.unlink()

    # 3. Add new file f3
    f3 = d / "c.txt"
    f3.write_text("new file", encoding="utf-8")

    res = verify_baseline(d, baseline_json)
    assert res["ok"] is False
    assert "a.txt" in res["modified"]
    assert "b.txt" in res["deleted"]
    assert "c.txt" in res["new"]


def test_verify_missing_baseline(tmp_path: Path):
    d = tmp_path / "project"
    d.mkdir()
    with pytest.raises(FileNotFoundError):
        verify_baseline(d, tmp_path / "nonexistent.json")


def test_exclusions_and_baseline_omission(tmp_path: Path):
    d = tmp_path / "project"
    d.mkdir()

    # Excluded dir
    git_dir = d / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("git config", encoding="utf-8")

    # Regular file
    f = d / "code.py"
    f.write_text("print('hello')", encoding="utf-8")

    baseline_json = d / "baseline.json"
    data = save_baseline(d, baseline_json)

    # Baseline file itself and .git should be excluded
    assert "baseline.json" not in data
    assert ".git/config" not in data
    assert "code.py" in data
