"""Caesar cipher encryption, decryption, and brute-force demo."""


def caesar_encrypt(text: str, shift: int = 3) -> str:
    """Encrypt text using Caesar cipher with given shift."""
    if not text:
        return ""

    # Normalize shift
    shift = shift % 26
    result = []

    for char in text:
        if "a" <= char <= "z":
            base = ord("a")
            shifted = chr((ord(char) - base + shift) % 26 + base)
            result.append(shifted)
        elif "A" <= char <= "Z":
            base = ord("A")
            shifted = chr((ord(char) - base + shift) % 26 + base)
            result.append(shifted)
        else:
            result.append(char)

    return "".join(result)


def caesar_decrypt(text: str, shift: int = 3) -> str:
    """Decrypt text using Caesar cipher with given shift."""
    return caesar_encrypt(text, -shift)


def caesar_brute_force(text: str) -> dict[int, str]:
    """Perform brute-force decryption across all 25 possible shifts."""
    results = {}
    for shift in range(1, 26):
        results[shift] = caesar_decrypt(text, shift)
    return results
