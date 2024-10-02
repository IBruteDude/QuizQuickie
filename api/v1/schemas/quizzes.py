"""JSON request validation schemas for the quizzes endpoints
"""

QUIZ_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": ["string", "null"]},
        "sort_by": {"type": ["string", "null"]},
        "difficulty": {"type": ["integer", "null"]},
        "group_id": {"type": ["integer", "null"]},
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
QUIZ_ONE_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
QUIZ_ONE_STATS_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
