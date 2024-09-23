#!/usr/bin/env python3
""" Module of the Base of Authentication mechanisms
"""
from typing import List, Tuple, TypeVar
from os import getenv
import base64

from models import storage
from models.user import User
from models.user_session import UserSession


class Auth:
    """Base authentication manager class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a path requires authentication"""
        if path is None or excluded_paths is None:
            return True
        if path in excluded_paths or path + "/" in excluded_paths:
            return False
        for expath in excluded_paths:
            if expath.endswith("*") and path.find(expath.strip("*")) != 0:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Extract the 'Authorization' header"""
        if request is None:
            return None
        if request.headers.get("Authorization") is None:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> User:
        """Get the current user"""
        return None

    def session_cookie(self, request=None):
        """Get the the cookie value of a request"""
        if request is None:
            return None
        return request.cookies.get(getenv("SESSION_NAME", "session_id"))
