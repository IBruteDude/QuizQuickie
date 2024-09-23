from flask import jsonify, request
from flask_babel import _

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.user_profile import (
    USER_PROFILE_GETTER_SCHEMA,
    USER_PROFILE_PUTTER_SCHEMA,
    USER_PROFILE_QUIZ_GETTER_SCHEMA,
    USER_PROFILE_QUIZ_POSTER_SCHEMA,
    USER_PROFILE_GROUP_GETTER_SCHEMA,
    USER_PROFILE_GROUP_POSTER_SCHEMA,
)


@app_routes.route("/api/v1/user/profile", methods=["GET"], strict_slashes=False)
def user_profile_getter():
    """GET /api/v1/user/profile
    Return:
      - on success: respond with user profile details
      - on error: respond with  error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_PROFILE_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "user": {
                            "email": "str",
                            "first_name": "str",
                            "last_name": "str",
                            "user_name": "str",
                            "profile_picture": "url",
                        }
                    }
                ),
                200,
            )
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/user/profile", methods=["PUT"], strict_slashes=False)
def user_profile_putter():
    """PUT /api/v1/user/profile
    Return:
      - on success: change user profile details
      - on error: respond with 400, 409 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_PROFILE_PUTTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return jsonify({}), 200
        case [400, err]:  # Stub for 400 response
            return jsonify({"error": _("invalid", data=_("profile"))}), 400
        case [409, err]:  # Stub for 409 response
            return jsonify({"error": _("duplicate", data=_("user_name"))}), 409
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/profile/quiz/<quiz_id>", methods=["GET"], strict_slashes=False
)
def user_profile_quiz_getter(quiz_id):
    """GET /api/v1/user/profile/quiz/<quiz_id>
    Return:
      - on success: respond with all user's quiz attempts
      - on error: respond with 403, 404, 410, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_PROFILE_QUIZ_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "total_pages": "int",
                        "total_attempts": "int",
                        "next": "int",
                        "prev": "int",
                        "attempts": [
                            {"attempt_id": "int", "time": "datetime", "score": "int"}
                        ],
                    }
                ),
                200,
            )
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case [410, err]:  # Stub for 410 response
            return jsonify({"error": _("deleted", data=_("quiz"))}), 410
        case [403, err]:  # Stub for 403 response
            return jsonify({"error": _("quiz time has ended")}), 403
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/profile/quiz/<quiz_id>", methods=["POST"], strict_slashes=False
)
def user_profile_quiz_poster(quiz_id):
    """POST /api/v1/user/profile/quiz/<quiz_id>
    Return:
      - on success: submit user answers for the quiz's questions
      - on error: respond with 404 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_PROFILE_QUIZ_POSTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "correct_answers": [
                            {"score": "int", "answers": [{"options": ["int"]}]}
                        ]
                    }
                ),
                200,
            )
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/user/profile/group", methods=["GET"], strict_slashes=False)
def user_profile_group_getter():
    """GET /api/v1/user/profile/group
    Return:
      - on success: respond with all the user's subscribed groups
      - on error: respond with 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_PROFILE_GROUP_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "total_pages": "int",
                        "total_groups": "int",
                        "next": "int",
                        "prev": "int",
                        "groups": [{"group_id": "int", "group_title": "str"}],
                    }
                ),
                200,
            )
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/user/profile/group", methods=["POST"], strict_slashes=False)
def user_profile_group_poster():
    """POST /api/v1/user/profile/group
    Return:
      - on success: subscribe the user to the group
      - on error: respond with 404, 409, 410 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_PROFILE_GROUP_POSTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return jsonify({"groups": [{"group_id": "int", "group_title": "str"}]}), 200
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        case [409, err]:  # Stub for 409 response
            return jsonify({"error": _("already subscribed to group")}), 409
        case [410, err]:  # Stub for 410 response
            return jsonify({"error": _("deleted", data=_("group"))}), 410
        case _:
            return jsonify({"error": _("unexpected")}), 500
