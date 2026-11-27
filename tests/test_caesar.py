"""Tests for Caesar cipher module."""

from cybershield.caesar import caesar_brute_force, caesar_decrypt, caesar_encrypt


def test_encrypt_basic():
    assert caesar_encrypt("abc", 1) == "bcd"
    assert caesar_encrypt("XYZ", 3) == "ABC"
    assert caesar_encrypt("Hello, World!", 3) == "Khoor, Zruog!"


def test_decrypt_basic():
    assert caesar_decrypt("bcd", 1) == "abc"
    assert caesar_decrypt("Khoor, Zruog!", 3) == "Hello, World!"


def test_round_trip():
    original = "Defensive Cybersecurity 101!"
    encrypted = caesar_encrypt(original, 7)
    decrypted = caesar_decrypt(encrypted, 7)
    assert decrypted == original


def test_empty_string():
    assert caesar_encrypt("", 5) == ""
    assert caesar_decrypt("", 5) == ""
    results = caesar_brute_force("")
    assert len(results) == 25
    assert all(v == "" for v in results.values())


def test_large_and_negative_shifts():
    assert caesar_encrypt("abc", 29) == caesar_encrypt("abc", 3)
    assert caesar_encrypt("abc", -1) == "zab"


def test_brute_force():
    encrypted = caesar_encrypt("secret", 5)
    results = caesar_brute_force(encrypted)
    assert len(results) == 25
    assert results[5] == "secret"
