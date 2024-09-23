from flask import jsonify, request
from flask_babel import _

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.groups import (
    GROUP_GETTER_SCHEMA,
    GROUP_USERS_GETTER_SCHEMA,
    GROUP_QUIZZES_GETTER_SCHEMA,
)


@app_routes.route("/api/v1/group", methods=["GET"], strict_slashes=False)
def group_getter():
    """GET /api/v1/group
    Return:
      - on success: respond with a list of available user groups
      - on error: respond with 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = GROUP_GETTER_SCHEMA
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
                        "groups": [
                            {
                                "group_id": "int",
                                "title": "str",
                                "owner_id": "int",
                                "owner_name": "str",
                            }
                        ],
                    }
                ),
                200,
            )
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/group/<group_id>/users", methods=["GET"], strict_slashes=False
)
def group_users_getter(group_id):
    """GET /api/v1/group/<group_id>/users
    Return:
      - on success: respond with a list of the groups subscribed users
      - on error: respond with 403, 404, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = GROUP_USERS_GETTER_SCHEMA
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
                        "users": [
                            {
                                "user_id": "int",
                                "user_name": "str",
                                "status": "str",
                                "score": "int",
                            }
                        ],
                    }
                ),
                200,
            )
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        case [403, err]:  # Stub for 403 response
            return jsonify({"error": _("unauthorized")}), 403
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/group/<group_id>/quizzes", methods=["GET"], strict_slashes=False
)
def group_quizzes_getter(group_id):
    """GET /api/v1/group/<group_id>/quizzes
    Return:
      - on success: respond with all the schedualed quizzes
      - on error: respond with 404, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = GROUP_QUIZZES_GETTER_SCHEMA
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
                                "start": "datetime",
                                "end": "datetime",
                            }
                        ],
                    }
                ),
                200,
            )
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500
