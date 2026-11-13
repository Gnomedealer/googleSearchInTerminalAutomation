"""Open URLs in the default browser or a specific one."""

import os
import webbrowser

# Common install locations on Windows. On macOS/Linux, Python's webbrowser
# module already knows these browsers by name.
_WINDOWS_PATHS = {
    "chrome": [r"Google\Chrome\Application\chrome.exe"],
    "edge": [r"Microsoft\Edge\Application\msedge.exe"],
    "firefox": [r"Mozilla Firefox\firefox.exe"],
    "brave": [r"BraveSoftware\Brave-Browser\Application\brave.exe"],
}


def _windows_candidates(name):
    roots = [os.environ.get(var) for var in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")]
    for root in filter(None, roots):
        for relative in _WINDOWS_PATHS.get(name, []):
            yield os.path.join(root, relative)


def find_browser(name):
    """Return a webbrowser controller for `name`, or None if it isn't found.

    `name` can be a browser name (chrome, edge, firefox, brave) or a path
    to the browser's .exe.
    """
    if os.path.isfile(name):
        return webbrowser.BackgroundBrowser(name)

    key = name.lower()
    for path in _windows_candidates(key):
        if os.path.isfile(path):
            return webbrowser.BackgroundBrowser(path)

    try:
        return webbrowser.get(key)
    except webbrowser.Error:
        return None


def open_url(url, browser=None):
    """Open the URL. Returns True on success.

    Raises LookupError if a specific browser was requested but not found.
    """
    if browser:
        controller = find_browser(browser)
        if controller is None:
            raise LookupError(f"Couldn't find the browser '{browser}'. Try chrome, edge, firefox, or a full path.")
        return controller.open(url)
    return webbrowser.open(url)
