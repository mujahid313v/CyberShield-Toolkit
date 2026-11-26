"""Password strength checker module."""

import re

COMMON_PASSWORDS = {
    "password",
    "123456",
    "12345678",
    "123456789",
    "12345",
    "1234567",
    "qwerty",
    "password1",
    "123123",
    "iloveyou",
    "admin",
    "welcome",
    "monkey",
    "dragon",
    "football",
    "baseball",
    "letmein",
    "trustno1",
    "master",
    "sunshine",
    "princess",
    "shadow",
    "secret",
}


def check_password_strength(password: str) -> dict[str, any]:
    """Evaluate password strength and return score, label, and suggestions."""
    if not password:
        return {
            "score": 0,
            "strength": "Very Weak",
            "suggestions": ["Password cannot be empty."],
        }

    score = 0
    suggestions: list[str] = []

    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    # 1. Common password check (exact or base match)
    pw_lower = password.lower()
    if pw_lower in COMMON_PASSWORDS or any(
        common in pw_lower for common in ["password", "123456", "qwerty"]
    ):
        return {
            "score": 5,
            "strength": "Very Weak",
            "suggestions": [
                "This password contains a common pattern or weak phrase. Choose a unique passphrase.",
                "Avoid common words, names, or simple number sequences.",
            ],
        }

    # 2. Length scoring (up to 40 points)
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 30
    elif length >= 8:
        score += 15
    else:
        score += 5
        suggestions.append(
            "Increase password length to at least 12 characters (16+ recommended)."
        )

    # 3. Character variety scoring (up to 40 points, 10 each)
    variety_count = sum([has_lower, has_upper, has_digit, has_special])
    score += variety_count * 10

    if not has_lower:
        suggestions.append("Add lowercase letters (a-z).")
    if not has_upper:
        suggestions.append("Add uppercase letters (A-Z).")
    if not has_digit:
        suggestions.append("Add numbers (0-9).")
    if not has_special:
        suggestions.append("Add special characters (e.g., !@#$%^&*).")

    # 4. Penalties for repetitive or sequential patterns
    if re.search(r"(.)\1{2,}", password):
        score -= 15
        suggestions.append(
            "Avoid repeating the same character 3 or more times consecutively."
        )

    sequences = [
        "123456",
        "234567",
        "345678",
        "456789",
        "abcd",
        "bcde",
        "cdef",
        "qwerty",
    ]
    if any(seq in pw_lower for seq in sequences):
        score -= 15
        suggestions.append("Avoid predictable keyboard sequences or number runs.")

    # Clamp score between 0 and 100
    score = max(0, min(100, score))

    # Determine strength label
    if score >= 80:
        strength = "Strong"
    elif score >= 60:
        strength = "Moderate"
    elif score >= 40:
        strength = "Weak"
    else:
        strength = "Very Weak"

    if not suggestions and score < 100:
        suggestions.append(
            "Great password! Consider using a password manager to store it securely."
        )

    return {
        "score": score,
        "strength": strength,
        "suggestions": suggestions,
    }
