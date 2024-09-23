from flask import jsonify, request
from flask_babel import _

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.quizzes import QUIZ_GETTER_SCHEMA, QUIZ_STATS_GETTER_SCHEMA


@app_routes.route("/api/v1/quiz", methods=["GET"], strict_slashes=False)
def quiz_getter():
    """GET /api/v1/quiz
    Return:
      - on success: respond with quizzes with different filters
      - on error: respond with 404, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = QUIZ_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "total_pages": "int",
                        "total_quizzes": "int",
                        "next": "int",
                        "prev": "int",
                        "quizzes": [
                            {
                                "quiz_id": "int",
                                "title": "str",
                                "category": "str",
                                "difficulty": "int",
                                "points": "int",
                                "duration?": "int",
                                "start?": "datetime",
                                "end?": "datetime",
                                "group_id?": "int",
                            }
                        ],
                    }
                ),
                200,
            )
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("category"))}), 404
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/quiz/<quiz_id>", methods=["GET"], strict_slashes=False)
def quiz_getter(quiz_id):
    """GET /api/v1/quiz/<quiz_id>
    Return:
      - on success: respond with the quiz's list of questions
      - on error: respond with 404, 410 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = QUIZ_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "questions": [
                            {
                                "statement": "str",
                                "points": "int",
                                "type": "str",
                                "options": ["str"],
                            }
                        ]
                    }
                ),
                200,
            )
        case [410, err]:  # Stub for 410 response
            return jsonify({"error": _("deleted", data=_("quiz"))}), 410
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/quiz/<quiz_id>/stats", methods=["GET"], strict_slashes=False)
def quiz_stats_getter(quiz_id):
    """GET /api/v1/quiz/<quiz_id>/stats
    Return:
      - on success: respond with stats about the user attempts of the quiz
      - on error: respond with 404 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = QUIZ_STATS_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "max_score": "float",
                        "min_score": "float",
                        "average_score": "float",
                        "attempts": "int",
                    }
                ),
                200,
            )
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500
