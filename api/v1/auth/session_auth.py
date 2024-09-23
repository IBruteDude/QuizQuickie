from datetime import timedelta, datetime
from os import getenv
import uuid

from api.v1.auth.auth import Auth
from models.user import User
from models.user_session import UserSession
from models import storage


class SessionAuth(Auth):
    """Session authentication manager class"""

    session_duration = int(getenv("SESSION_DURATION", 86400))

    def create_session(self, user_id: str = None) -> str:
        """Create a session id associated with a user id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())

        storage.new(
            UserSession(
                expiry_date=(datetime.now() + timedelta(seconds=self.session_duration)),
                uuid=session_id,
                user_id=user_id,
            )
        )
        return session_id

    def current_user(self, request) -> User:
        """Get the current user"""
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None
        session = (
            storage.query(UserSession)
            .where(UserSession.uuid == session_cookie)
            .one_or_none()
        )
        if session is None:
            return None
        if session.expiry_date <= datetime.now():
            storage.delete(session)
            return None
        user = storage.query(User).where(User.id == session.user_id).one_or_none()
        return user

    def destroy_session(self, request) -> bool:
        """destroy the session/log out the current user
        Return:
            - on success: True
            - on error: False
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False

        user_session = (
            storage.query(UserSession).filter_by(uuid=session_cookie).one_or_none()
        )
        if user_session is None:
            return False
        storage.delete(user_session)
        return True
