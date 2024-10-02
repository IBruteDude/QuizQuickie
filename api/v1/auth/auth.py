#!/usr/bin/env python3
""" Module of the Base of Authentication mechanisms
"""
from os import getenv
import base64

from models import storage
from models.user import User
from models.user_session import UserSession


class Auth:
    """Base authentication manager class"""

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
