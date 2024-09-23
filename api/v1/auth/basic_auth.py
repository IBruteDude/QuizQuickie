from typing import Tuple
from api.v1.auth.auth import Auth
import base64

import bcrypt

from models.user import User
from models import storage


class BasicAuth(Auth):
    """Basic authentication manager class"""

    def extract_auth_header(self, auth_header: str) -> str:
        """Get the auth header base64 encoded part"""
        if auth_header is None:
            return None
        if type(auth_header) is not str:
            return None
        if auth_header[:6] != "Basic ":
            return None
        return auth_header[6:]

    def decode_header(self, auth_header: str) -> str:
        """Get the decoded base64 encoded auth header part"""
        if auth_header is None:
            return None
        if type(auth_header) is not str:
            return None

        try:
            return base64.decodebytes(auth_header.encode()).decode()
        except Exception:
            return None

    def extract_user_credentials(self, auth_header: str) -> Tuple[str, str]:
        """Extract the user email and password from header"""
        if auth_header is None:
            return None, None
        if type(auth_header) is not str:
            return None, None
        semicolon = auth_header.find(":")
        if semicolon == -1:
            return None, None

        return (auth_header[:semicolon], auth_header[semicolon + 1 :])

    def user_object_from_credentials(self, email: str, password: str) -> User:
        """Create a User instance with specified credentials"""
        if email is None or password is None:
            return None
        if type(email) is not str or type(password) is not str:
            return None
        user: User = storage.query(User).filter_by(email=email).one_or_none()

        if user is None:
            return None
        if not bcrypt.checkpw(password.encode(), user.password):
            return None
        return user

    def current_user(self, request) -> User:
        """Get the current user authorized for a request"""
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        b64_header = self.extract_auth_header(auth_header)
        header_data = self.decode_header(b64_header)
        user_email, user_pwd = self.extract_user_credentials(header_data)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
