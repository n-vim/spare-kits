from {{ package_name }} import slugify


def test_slugify() -> None:
    assert slugify("Hello SpareKit!!") == "hello-sparekit"
