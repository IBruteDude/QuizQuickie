from flask import jsonify, request
from flask_babel import _

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.profiles import PROFILE_GETTER_SCHEMA, PROFILE_QUIZ_GETTER_SCHEMA


@app_routes.route("/api/v1/profile", methods=["GET"], strict_slashes=False)
def profile_getter():
    """GET /api/v1/profile
    Return:
      - on success: respond with quizzes with different filters
      - on error: respond with 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = PROFILE_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "total_pages": "int",
                        "total_users": "int",
                        "next": "int",
                        "prev": "int",
                        "users": [{"user_id": "int", "user_name": "str"}],
                    }
                ),
                200,
            )
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/profile/<user_id>", methods=["GET"], strict_slashes=False)
def profile_getter(user_id):
    """GET /api/v1/profile/<user_id>
    Return:
      - on success: respond with user profile info
      - on error: respond with 404 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = PROFILE_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "user_name": "str",
                        "owned_groups": "int",
                        "created_quizzes": "int",
                        "subscribed_groups": "int",
                        "solved_quizzes": "int",
                    }
                ),
                200,
            )
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("user"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/profile/<user_id>/quiz", methods=["GET"], strict_slashes=False
)
def profile_quiz_getter(user_id):
    """GET /api/v1/profile/<user_id>/quiz
    Return:
      - on success: respond with the user's created quizzes
      - on error: respond with 404, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = PROFILE_QUIZ_GETTER_SCHEMA
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
                                "duration": "int",
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
