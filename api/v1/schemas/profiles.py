"""JSON request validation schemas for the profiles endpoints
"""

PROFILE_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
PROFILE_QUIZ_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string"},
        "sort_by": {"type": "string"},
        "difficulty": {"type": "integer"},
        "page": {"type": "integer"},
        "page_size": {"type": "integer"},
        "query": {"type": "string"},
    },
    "required": [],
}
