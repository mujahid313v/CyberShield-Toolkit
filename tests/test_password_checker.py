"""Tests for password strength checker module."""

from cybershield.password_checker import check_password_strength


def test_empty_password():
    result = check_password_strength("")
    assert result["score"] == 0
    assert result["strength"] == "Very Weak"
    assert "cannot be empty" in result["suggestions"][0]


def test_common_password():
    result = check_password_strength("password")
    assert result["score"] <= 10
    assert result["strength"] == "Very Weak"
    assert any("common" in s.lower() for s in result["suggestions"])


def test_weak_password():
    result = check_password_strength("abc")
    assert result["score"] < 40
    assert result["strength"] == "Very Weak"


def test_moderate_password():
    result = check_password_strength("Pass1")
    assert 0 <= result["score"] < 80
    assert result["strength"] in ["Weak", "Very Weak"]


def test_strong_password():
    result = check_password_strength("P@ssw0rd123!SecurePass")
    assert result["score"] >= 80
    assert result["strength"] == "Strong"


def test_repetitive_penalty():
    result1 = check_password_strength("Abcd1234!@#$")
    result2 = check_password_strength("Abcd1234!@#$aaaa")
    assert result2["score"] < result1["score"]


def test_sequential_penalty():
    result1 = check_password_strength("P@ssw0rd.xyz789")
    result2 = check_password_strength("P@ssw0rd.123456")
    assert result2["score"] < result1["score"]
