"""JSON request validation schemas for the user_groups endpoints
"""

USER_GROUP_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
USER_GROUP_POSTER_SCHEMA = {
    "type": "object",
    "properties": {"title": {"type": "string", "pattern": "^(?!\\s*$).+"}},
    "required": ["title"],
}
USER_GROUP_ONE_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
USER_GROUP_ONE_PUTTER_SCHEMA = {
    "type": "object",
    "properties": {"title": {"type": "string", "pattern": "^(?!\\s*$).+"}},
    "required": ["title"],
}
USER_GROUP_ONE_DELETER_SCHEMA = {"type": "object", "properties": {}, "required": []}
USER_GROUP_ONE_USERS_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
USER_GROUP_ONE_USERS_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "users": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"user_id": {"type": "integer"}},
                "required": ["user_id"],
            },
        }
    },
    "required": ["users"],
}
USER_GROUP_ONE_USERS_DELETER_SCHEMA = {
    "type": "object",
    "properties": {
        "users": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"user_id": {"type": "integer"}},
                "required": ["user_id"],
            },
        }
    },
    "required": ["users"],
}
