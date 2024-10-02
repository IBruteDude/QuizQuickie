"""JSON request validation schemas for the groups endpoints
"""

GROUP_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
GROUP_ONE_USERS_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "sort_by": {"type": ["string", "null"]},
        "status": {"type": ["string", "null"]},
        "max_score": {"type": ["integer", "null"]},
        "min_score": {"type": ["integer", "null"]},
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
GROUP_ONE_QUIZZES_GETTER_SCHEMA = {
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
