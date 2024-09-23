"""JSON request validation schemas for the user_auth endpoints
"""

AUTH_SIGNUP_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "user_name": {"type": "string"},
        "profile_picture": {
            "type": "string",
            "pattern": "^(https?|ftp|file)://([-a-zA-Z0-9@:%._+~#=]{2,256})(:[0-9]+)?(/[-a-zA-Z0-9@:%._+~#=]*)*$",
        },
    },
    "required": ["email", "password", "first_name", "last_name", "user_name"],
}
AUTH_LOGIN_POSTER_SCHEMA = {
    "type": "object",
    "properties": {"email": {"type": "string"}, "password": {"type": "string"}},
    "required": ["email", "password"],
}
AUTH_PASSWORD_RESET_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
AUTH_PASSWORD_RESET_CONFIRM_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "reset_token": {"type": "string"},
        "new_password": {"type": "string"},
    },
    "required": ["reset_token", "new_password"],
}
AUTH_LOGOUT_DELETER_SCHEMA = {"type": "object", "properties": {}, "required": []}
AUTH_DEACTIVATE_DELETER_SCHEMA = {"type": "object", "properties": {}, "required": []}
