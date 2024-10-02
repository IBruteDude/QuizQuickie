"""JSON request validation schemas for the user_profile endpoints
"""

USER_PROFILE_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
USER_PROFILE_PUTTER_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": ["string", "null"]},
        "last_name": {"type": ["string", "null"]},
        "user_name": {"type": ["string", "null"]},
        "profile_picture": {"type": ["string", "null"], "format": "uri"},
    },
    "required": [],
}
USER_PROFILE_QUIZ_ONE_ATTEMPTS_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
USER_PROFILE_QUIZ_ONE_ATTEMPTS_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "answers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "options": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["options"],
            },
        }
    },
    "required": ["answers"],
}
USER_PROFILE_GROUP_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
USER_PROFILE_GROUP_POSTER_SCHEMA = {
    "type": "object",
    "properties": {"group_id": {"type": "integer"}},
    "required": ["group_id"],
}
USER_PROFILE_GROUP_ONE_DELETER_SCHEMA = {
    "type": "object",
    "properties": {},
    "required": [],
}
