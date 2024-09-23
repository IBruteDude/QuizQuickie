"""JSON request validation schemas for the user_profile endpoints
"""

USER_PROFILE_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
USER_PROFILE_PUTTER_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "user_name": {"type": "string"},
        "profile_picture": {
            "type": "string",
            "pattern": "^(https?|ftp|file)://([-a-zA-Z0-9@:%._+~#=]{2,256})(:[0-9]+)?(/[-a-zA-Z0-9@:%._+~#=]*)*$",
        },
    },
    "required": [],
}
USER_PROFILE_QUIZ_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "page_size": {"type": "integer"},
        "query": {"type": "string"},
    },
    "required": [],
}
USER_PROFILE_QUIZ_POSTER_SCHEMA = {
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
        "page": {"type": "integer"},
        "page_size": {"type": "integer"},
        "query": {"type": "string"},
    },
    "required": [],
}
USER_PROFILE_GROUP_POSTER_SCHEMA = {
    "type": "object",
    "properties": {"group_id": {"type": "integer"}},
    "required": ["group_id"],
}
