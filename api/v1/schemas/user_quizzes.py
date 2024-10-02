"""JSON request validation schemas for the user_quizzes endpoints
"""

USER_QUIZ_GETTER_SCHEMA = {
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
USER_QUIZ_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "pattern": "^(?!\\s*$).+"},
        "category": {"type": "string", "pattern": "^(?!\\s*$).+"},
        "difficulty": {"type": "integer"},
        "points": {"type": "integer"},
        "duration": {"type": ["integer", "null"]},
        "start": {"type": ["string", "null"], "format": "date-time"},
        "end": {"type": ["string", "null"], "format": "date-time"},
        "group_id": {"type": ["integer", "null"]},
    },
    "required": ["title", "category", "difficulty", "points"],
}
USER_QUIZ_ONE_GETTER_SCHEMA = {"type": "object", "properties": {}, "required": []}
USER_QUIZ_ONE_PUTTER_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": ["string", "null"]},
        "category": {"type": ["string", "null"]},
        "difficulty": {"type": ["integer", "null"]},
        "points": {"type": ["integer", "null"]},
        "duration": {"type": ["integer", "null"]},
        "start": {"type": ["string", "null"], "format": "date-time"},
        "end": {"type": ["string", "null"], "format": "date-time"},
        "group_id": {"type": ["integer", "null"]},
    },
    "required": [],
}
USER_QUIZ_ONE_DELETER_SCHEMA = {"type": "object", "properties": {}, "required": []}
USER_QUIZ_ONE_QUESTION_GETTER_SCHEMA = {
    "type": "object",
    "properties": {},
    "required": [],
}
USER_QUIZ_ONE_QUESTION_POSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "statement": {"type": "string", "pattern": "^(?!\\s*$).+"},
                    "points": {"type": "integer"},
                    "type": {"type": "string", "pattern": "^(?!\\s*$).+"},
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
USER_QUIZ_ONE_QUESTION_PUTTER_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question_id": {"type": "integer"},
                    "statement": {"type": ["string", "null"]},
                    "points": {"type": ["integer", "null"]},
                    "type": {"type": ["string", "null"]},
                    "options": {"type": ["array", "null"], "items": {"type": "string"}},
                    "correct_answer": {
                        "type": ["array", "null"],
                        "items": {"type": "integer"},
                    },
                },
                "required": ["question_id"],
            },
        }
    },
    "required": ["questions"],
}
USER_QUIZ_ONE_QUESTION_DELETER_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"question_id": {"type": "integer"}},
                "required": ["question_id"],
            },
        }
    },
    "required": ["questions"],
}
USER_QUIZ_ONE_STATS_ATTEMPTS_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
USER_QUIZ_ONE_STATS_QUESTION_ONE_GETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": ["integer", "null"]},
        "page_size": {"type": ["integer", "null"]},
        "query": {"type": ["string", "null"]},
    },
    "required": [],
}
