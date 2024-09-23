"""JSON request validation schemas for the user_quizzes endpoints
"""

USER_QUIZ_GETTER_SCHEMA = {
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
USER_QUIZ_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "category": {"type": "string"},
        "difficulty": {"type": "integer"},
        "points": {"type": "integer"},
        "duration": {"type": "integer"},
        "start": {"type": "string", "pattern": ""},
        "end": {"type": "string", "pattern": ""},
        "group_id": {"type": "integer"},
    },
    "required": ["title", "category", "difficulty", "points"],
}
USER_QUIZ_PUTTER_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "category": {"type": "string"},
        "difficulty": {"type": "integer"},
        "points": {"type": "integer"},
        "duration": {"type": "integer"},
        "start": {"type": "string", "pattern": ""},
        "end": {"type": "string", "pattern": ""},
        "group_id": {"type": "integer"},
    },
    "required": [],
}
USER_QUIZ_DELETER_SCHEMA = {"type": "object", "properties": {}, "required": []}
USER_QUIZ_QUESTION_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
USER_QUIZ_QUESTION_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "statement": {"type": "string"},
                    "points": {"type": "integer"},
                    "type": {"type": "string"},
                    "options": {"type": "array", "items": {"type": "string"}},
                    "correct_answer": {"type": "array", "items": {"type": "integer"}},
                },
                "required": [
                    "statement",
                    "points",
                    "type",
                    "options",
                    "correct_answer",
                ],
            },
        }
    },
    "required": ["questions"],
}
USER_QUIZ_QUESTION_PUTTER_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "number": {"type": "integer"},
                    "statement": {"type": "string"},
                    "points": {"type": "integer"},
                    "type": {"type": "string"},
                    "options": {"type": "array", "items": {"type": "string"}},
                    "correct_answer": {"type": "array", "items": {"type": "integer"}},
                },
                "required": ["number"],
            },
        }
    },
    "required": ["questions"],
}
USER_QUIZ_QUESTION_DELETER_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"number": {"type": "integer"}},
                "required": ["number"],
            },
        }
    },
    "required": ["question"],
}
USER_QUIZ_STATS_ATTEMPTS_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "page_size": {"type": "integer"},
        "query": {"type": "string"},
    },
    "required": [],
}
USER_QUIZ_STATS_QUESTION_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "page_size": {"type": "integer"},
        "query": {"type": "string"},
    },
    "required": [],
}
