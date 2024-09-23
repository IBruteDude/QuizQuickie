from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from os import getenv


match getenv("AUTH", None):
    case "BASIC_AUTH":
        auth = BasicAuth()
    case "SESSION_AUTH":
        auth = SessionAuth()
    case None:
        auth = None
