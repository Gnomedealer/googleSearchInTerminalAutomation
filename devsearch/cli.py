"""Command-line interface for devsearch."""

import argparse
import os
import sys

from . import __version__
from .browsers import open_url
from .search import DEFAULT_SITES, ENGINES, build_query, build_url, choose_sites, normalize_site


def _site(value):
    """argparse type: validate and clean up a site name."""
    try:
        return normalize_site(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error))


def default_sites():
    """Default sites, overridable with DEVSEARCH_SITES=site1,site2"""
    env = os.environ.get("DEVSEARCH_SITES", "").strip()
    if not env:
        return DEFAULT_SITES
    return [normalize_site(s) for s in env.split(",") if s.strip()]


def build_parser():
    parser = argparse.ArgumentParser(
        prog="devsearch",
        description="Search the web for coding answers, focused on developer sites "
        "like Stack Overflow and Reddit.",
        epilog=(
            "examples:\n"
            '  devsearch how to reverse a list in python\n'
            '  devsearch "c++ vs c#" -e duckduckgo\n'
            "  devsearch useEffect cleanup -s react.dev -s github.com\n"
            "  devsearch css grid gap --add developer.mozilla.org\n"
            "  devsearch rust borrow checker --all --print"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", nargs="*", help="what to search for")

    sites = parser.add_argument_group("choosing sites")
    sites.add_argument("-s", "--site", action="append", type=_site, metavar="SITE",
                       help="search only this site (repeat for several); replaces the defaults")
    sites.add_argument("-a", "--add", action="append", type=_site, metavar="SITE",
                       help="add a site to the defaults")
    sites.add_argument("-x", "--exclude", action="append", type=_site, metavar="SITE",
                       help="leave a site out")
    sites.add_argument("--all", action="store_true", help="search the whole web (no site filter)")
    sites.add_argument("--list-sites", action="store_true", help="show the default sites and exit")

    parser.add_argument("-e", "--engine", choices=sorted(ENGINES), default="google",
                        help="search engine to use (default: google)")
    parser.add_argument("-b", "--browser", metavar="NAME",
                        help="browser to open: chrome, edge, firefox, brave, or a path (default: your default browser)")
    parser.add_argument("-p", "--print", dest="print_only", action="store_true",
                        help="print the search link instead of opening a browser")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        defaults = default_sites()
    except ValueError as error:
        parser.error(f"DEVSEARCH_SITES: {error}")

    if args.list_sites:
        print("Default sites:")
        for site in defaults:
            print(f"  {site}")
        return 0

    if not args.query:
        parser.print_usage(sys.stderr)
        print('devsearch: error: tell me what to search for, e.g. devsearch "how to reverse a list"', file=sys.stderr)
        return 2

    sites = choose_sites(defaults, only=args.site, add=args.add, exclude=args.exclude, everywhere=args.all)
    query = build_query(args.query, sites)
    url = build_url(query, args.engine)

    if args.print_only:
        print(url)
        return 0

    where = ", ".join(sites) if sites else "the whole web"
    print(f'Searching {args.engine} for "{" ".join(args.query)}" on {where}')
    try:
        opened = open_url(url, args.browser)
    except LookupError as error:
        print(f"devsearch: error: {error}", file=sys.stderr)
        return 1
    if not opened:
        print("devsearch: couldn't open a browser. Here's the link:", file=sys.stderr)
        print(url)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
