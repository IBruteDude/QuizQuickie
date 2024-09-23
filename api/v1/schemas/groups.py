"""JSON request validation schemas for the groups endpoints
"""

GROUP_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "page_size": {"type": "integer"},
        "query": {"type": "string"},
    },
    "required": [],
}
GROUP_USERS_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "sort_by": {"type": "string"},
        "status": {"type": "string"},
        "max_score": {"type": "integer"},
        "min_score": {"type": "integer"},
        "page": {"type": "integer"},
        "page_size": {"type": "integer"},
        "query": {"type": "string"},
    },
    "required": [],
}
GROUP_QUIZZES_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "page_size": {"type": "integer"},
        "query": {"type": "string"},
    },
    "required": [],
}
