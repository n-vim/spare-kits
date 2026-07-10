from {{ package_name }}.core import build_greeting, count_words


def test_build_greeting() -> None:
    assert build_greeting("Nitish") == "Hello, Nitish!"


def test_build_greeting_excited() -> None:
    assert build_greeting("Nitish", excited=True) == "HELLO, NITISH!"


def test_count_words() -> None:
    assert count_words("hello from sparekit") == 3
