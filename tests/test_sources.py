from pathlib import Path

import pytest

from sparekit.exceptions import TemplateSourceError
from sparekit.sources import open_template_source, parse_github_source


def test_parse_github_source_basic() -> None:
    parsed = parse_github_source("github:n-vim/spare-kits/src/sparekit/templates")
    assert parsed.clone_url == "https://github.com/n-vim/spare-kits.git"
    assert parsed.ref is None
    assert parsed.subpath == Path("src/sparekit/templates")


def test_parse_github_source_with_ref() -> None:
    parsed = parse_github_source("github:n-vim/spare-kits@main/templates")
    assert parsed.ref == "main"
    assert parsed.subpath == Path("templates")


def test_open_template_source_local_missing() -> None:
    with pytest.raises(TemplateSourceError):
        with open_template_source("local:/definitely/missing/sparekit"):
            pass
