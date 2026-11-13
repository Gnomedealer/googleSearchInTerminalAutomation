# devsearch

Search for coding answers from your terminal. `devsearch` opens a web search focused on the sites where developers actually find answers: **Stack Overflow, Stack Exchange, Reddit, and Medium**.

```bash
devsearch how to reverse a list in python
```

This opens your browser to a search for *"how to reverse a list in python"* limited to those sites.

## Install

Requires Python 3.9+.

```bash
git clone https://github.com/Gnomedealer/googleSearchInTerminalAutomation.git
cd googleSearchInTerminalAutomation
python -m venv .venv
.venv\Scripts\activate        # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -e .
```

Now `devsearch` works anywhere while the environment is active. You can also run it without installing: `python main.py <your search>`.

## Usage

| Command | What it does |
|---|---|
| `devsearch useEffect cleanup` | Search the default developer sites |
| `devsearch "c++ vs c#"` | Special characters are handled correctly |
| `devsearch hooks -s react.dev -s github.com` | Search **only** these sites |
| `devsearch css grid --add developer.mozilla.org` | Add a site to the defaults |
| `devsearch python tips -x medium.com` | Leave a site out |
| `devsearch rust borrow checker --all` | Search the whole web |
| `devsearch flexbox -e duckduckgo` | Use DuckDuckGo or Bing instead of Google |
| `devsearch regex lookahead -b firefox` | Open in a specific browser (chrome, edge, firefox, brave, or a path) |
| `devsearch git rebase --print` | Print the link instead of opening it |
| `devsearch --list-sites` | Show the default sites |
| `devsearch --help` | Full help |

### Change the default sites

Set `DEVSEARCH_SITES` to a comma-separated list:

```bash
# Windows PowerShell
$env:DEVSEARCH_SITES = "stackoverflow.com,github.com,docs.python.org"
# macOS/Linux
export DEVSEARCH_SITES="stackoverflow.com,github.com,docs.python.org"
```

## Development

```bash
pip install -e ".[dev]"
pytest            # 32 tests
```

```
devsearch/
  search.py     building the query and URL (site filters, engines, encoding)
  browsers.py   finding and opening browsers
  cli.py        command-line options and output
tests/          pytest tests for both
main.py         run without installing
```

## Author

**Tommy Nguyen**: [github.com/Gnomedealer](https://github.com/Gnomedealer)
