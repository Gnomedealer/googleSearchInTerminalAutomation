from urllib.parse import parse_qs, urlparse

import pytest

from devsearch.search import (
    DEFAULT_SITES,
    build_query,
    build_url,
    choose_sites,
    normalize_site,
    site_filter,
)


def query_param(url):
    """Decode the q= part of a search URL back into plain text."""
    return parse_qs(urlparse(url).query)["q"][0]


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("github.com", "github.com"),
        ("https://www.GitHub.com/", "github.com"),
        ("http://docs.python.org/3/library", "docs.python.org"),
        ("  React.dev  ", "react.dev"),
    ],
)
def test_normalize_site(raw, expected):
    assert normalize_site(raw) == expected


@pytest.mark.parametrize("bad", ["github", "", "not a site", ".com", "github."])
def test_normalize_site_rejects_bad_input(bad):
    with pytest.raises(ValueError):
        normalize_site(bad)


def test_site_filter():
    assert site_filter(["a.com", "b.com"]) == "(site:a.com OR site:b.com)"
    assert site_filter(["a.com"]) == "(site:a.com)"
    assert site_filter([]) == ""


def test_choose_sites_defaults():
    assert choose_sites() == DEFAULT_SITES


def test_choose_sites_only_replaces_defaults():
    assert choose_sites(only=["github.com"]) == ["github.com"]


def test_choose_sites_add_and_exclude_without_duplicates():
    sites = choose_sites(add=["github.com", "reddit.com"], exclude=["medium.com"])
    assert sites == ["stackoverflow.com", "stackexchange.com", "reddit.com", "github.com"]


def test_choose_sites_everywhere():
    assert choose_sites(only=["github.com"], everywhere=True) == []


def test_build_query_adds_space_before_filter():
    # The original script glued the filter onto the last word ("list(site:...").
    assert build_query(["reverse", "a", "list"], ["a.com"]) == "reverse a list (site:a.com)"


def test_build_query_without_sites():
    assert build_query(["hello"], []) == "hello"


def test_build_query_requires_text():
    with pytest.raises(ValueError):
        build_query(["  "], DEFAULT_SITES)


def test_build_url_encodes_special_characters():
    # The original bug: + # & weren't encoded, so these searches broke.
    query = "c++ vs c# & rust?"
    url = build_url(query)
    assert url.startswith("https://www.google.com/search?q=")
    assert "#" not in url and "&" not in url.split("?q=")[1]
    assert query_param(url) == query


@pytest.mark.parametrize(
    "engine, host",
    [("google", "www.google.com"), ("duckduckgo", "duckduckgo.com"), ("bing", "www.bing.com")],
)
def test_build_url_engines(engine, host):
    assert urlparse(build_url("test", engine)).netloc == host


def test_build_url_unknown_engine():
    with pytest.raises(ValueError):
        build_url("test", "altavista")
