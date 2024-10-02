"""JSON request validation schemas for the auth endpoints
"""

AUTH_SIGNUP_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email", "pattern": "^(?!\\s*$).+"},
        "password": {"type": "string", "pattern": "^(?!\\s*$).+"},
        "first_name": {"type": "string", "pattern": "^(?!\\s*$).+"},
        "last_name": {"type": "string", "pattern": "^(?!\\s*$).+"},
        "user_name": {"type": "string", "pattern": "^(?!\\s*$).+"},
        "profile_picture": {"type": ["string", "null"], "format": "uri"},
    },
    "required": ["email", "password", "first_name", "last_name", "user_name"],
}
AUTH_LOGIN_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email", "pattern": "^(?!\\s*$).+"},
        "password": {"type": "string", "pattern": "^(?!\\s*$).+"},
    },
    "required": ["email", "password"],
}
AUTH_PASSWORD_RESET_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
AUTH_PASSWORD_RESET_CONFIRM_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "reset_token": {"type": "string", "pattern": "^(?!\\s*$).+"},
        "new_password": {"type": "string", "pattern": "^(?!\\s*$).+"},
    },
    "required": ["reset_token", "new_password"],
}
AUTH_LOGOUT_DELETER_SCHEMA = {"type": "object", "properties": {}, "required": []}
AUTH_DEACTIVATE_DELETER_SCHEMA = {"type": "object", "properties": {}, "required": []}
