"""JSON request validation schemas for the profiles endpoints
"""

PROFILE_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
PROFILE_ONE_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
PROFILE_ONE_QUIZ_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": ["string", "null"]},
        "sort_by": {"type": ["string", "null"]},
        "difficulty": {"type": ["integer", "null"]},
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
