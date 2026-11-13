"""Build search URLs that focus on developer Q&A sites."""

from urllib.parse import quote_plus

DEFAULT_SITES = [
    "stackoverflow.com",
    "stackexchange.com",
    "reddit.com",
    "medium.com",
]

ENGINES = {
    "google": "https://www.google.com/search?q={}",
    "duckduckgo": "https://duckduckgo.com/?q={}",
    "bing": "https://www.bing.com/search?q={}",
}


def normalize_site(site):
    """Turn 'https://www.GitHub.com/' into 'github.com'.

    Raises ValueError if it doesn't look like a domain.
    """
    cleaned = site.strip().lower()
    for prefix in ("https://", "http://"):
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
    if cleaned.startswith("www."):
        cleaned = cleaned[4:]
    cleaned = cleaned.split("/")[0]
    if "." not in cleaned or " " in cleaned or cleaned.startswith(".") or cleaned.endswith("."):
        raise ValueError(f"'{site}' doesn't look like a website (expected something like github.com)")
    return cleaned


def choose_sites(defaults=None, only=None, add=None, exclude=None, everywhere=False):
    """Work out which sites to search, keeping order and dropping duplicates."""
    if everywhere:
        return []
    sites = list(only) if only else list(DEFAULT_SITES if defaults is None else defaults)
    sites += list(add or [])
    excluded = set(exclude or [])

    result = []
    for site in sites:
        if site not in excluded and site not in result:
            result.append(site)
    return result


def site_filter(sites):
    """['a.com', 'b.com'] -> '(site:a.com OR site:b.com)'"""
    if not sites:
        return ""
    return "(" + " OR ".join(f"site:{site}" for site in sites) + ")"


def build_query(terms, sites):
    """Combine the search words with the site filter."""
    text = " ".join(terms).strip()
    if not text:
        raise ValueError("Please provide something to search for.")
    filt = site_filter(sites)
    return f"{text} {filt}" if filt else text


def build_url(query, engine="google"):
    """Make a safe search URL. quote_plus encodes characters like + # & ?"""
    if engine not in ENGINES:
        raise ValueError(f"Unknown search engine '{engine}'. Choose from: {', '.join(ENGINES)}")
    return ENGINES[engine].format(quote_plus(query))
