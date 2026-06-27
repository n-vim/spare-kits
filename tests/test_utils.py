from sparekit.utils import normalize_distribution_name, normalize_package_name, render_string


def test_normalize_package_name() -> None:
    assert normalize_package_name("My Cool-App") == "my_cool_app"
    assert normalize_package_name("123 demo") == "app_123_demo"
    assert normalize_package_name("!!!") == "app"


def test_normalize_distribution_name() -> None:
    assert normalize_distribution_name("My Cool_App") == "my-cool-app"
    assert normalize_distribution_name("...") == "app"


def test_render_string_replaces_known_tokens() -> None:
    assert render_string("Hello {{ name }}", {"name": "Nitish"}) == "Hello Nitish"


def test_render_string_keeps_unknown_tokens() -> None:
    assert render_string("Hello {{ missing }}", {}) == "Hello {{ missing }}"
