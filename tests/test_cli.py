from urllib.parse import parse_qs, urlparse

import pytest

from devsearch import cli


@pytest.fixture
def opened(monkeypatch):
    """Capture URLs instead of actually opening a browser."""
    calls = []

    def fake_open(url, browser=None):
        calls.append((url, browser))
        return True

    monkeypatch.setattr(cli, "open_url", fake_open)
    monkeypatch.delenv("DEVSEARCH_SITES", raising=False)
    return calls


def q(url):
    return parse_qs(urlparse(url).query)["q"][0]


def test_opens_browser_with_default_sites(opened, capsys):
    assert cli.main(["how", "to", "reverse", "a", "list"]) == 0
    url, browser = opened[0]
    assert q(url).startswith("how to reverse a list (site:stackoverflow.com OR")
    assert browser is None
    assert "Searching google" in capsys.readouterr().out


def test_print_only_does_not_open(opened, capsys):
    assert cli.main(["css", "grid", "--print"]) == 0
    assert opened == []
    out = capsys.readouterr().out.strip()
    assert out.startswith("https://www.google.com/search?q=")


def test_specific_sites_and_engine(opened):
    cli.main(["hooks", "-s", "react.dev", "-s", "https://www.github.com/", "-e", "duckduckgo"])
    url, _ = opened[0]
    assert urlparse(url).netloc == "duckduckgo.com"
    assert q(url) == "hooks (site:react.dev OR site:github.com)"


def test_all_searches_whole_web(opened):
    cli.main(["rust", "--all"])
    assert q(opened[0][0]) == "rust"


def test_browser_option_is_passed_through(opened):
    cli.main(["test", "-b", "firefox"])
    assert opened[0][1] == "firefox"


def test_missing_query_is_a_friendly_error(opened, capsys):
    assert cli.main([]) == 2
    assert "tell me what to search for" in capsys.readouterr().err
    assert opened == []


def test_bad_site_is_rejected(opened, capsys):
    with pytest.raises(SystemExit) as exit_info:
        cli.main(["test", "-s", "notasite"])
    assert exit_info.value.code == 2
    assert "doesn't look like a website" in capsys.readouterr().err


def test_list_sites(opened, capsys):
    assert cli.main(["--list-sites"]) == 0
    out = capsys.readouterr().out
    assert "stackoverflow.com" in out and "reddit.com" in out


def test_env_var_overrides_default_sites(opened, monkeypatch):
    monkeypatch.setenv("DEVSEARCH_SITES", "github.com, docs.python.org")
    cli.main(["asyncio"])
    assert q(opened[0][0]) == "asyncio (site:github.com OR site:docs.python.org)"


def test_unknown_browser_reports_error(monkeypatch, capsys):
    monkeypatch.setattr(cli, "open_url", lambda url, browser=None: (_ for _ in ()).throw(LookupError("Couldn't find the browser 'nope'.")))
    assert cli.main(["test", "-b", "nope"]) == 1
    assert "Couldn't find the browser" in capsys.readouterr().err
