from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

from os import getenv
from typing import List

from werkzeug.routing import Map, Rule


def require_auth(path: str, excluded_paths: List[str]) -> bool:
    """Check if a path requires authentication using Werkzeug route matching."""
    if path is None or excluded_paths is None:
        return True

    # Create a URL map for excluded paths
    url_map = Map()

    # Normalise path slashes
    path = path.rstrip("/")

    for ep in excluded_paths:
        # Replace wildcard '*' with '<path:rest>' to match anything after the base path
        ep = ep.rstrip("/")
        if ep.endswith("/*"):
            ep = ep.rstrip("*") + "<path:rest>"
        url_map.add(Rule(ep))

    matcher = url_map.bind("", "/")  # Adjust the host/path if necessary

    # Check if the path matches any of the excluded paths
    try:
        matcher.match(path)
        return False  # Path is excluded
    except Exception:
        return True  # Path requires authentication


match getenv("AUTH", None):
    case "BASIC_AUTH":
        auth = BasicAuth()
    case "SESSION_AUTH":
        auth = SessionAuth()
    case None:
        auth = Auth()
