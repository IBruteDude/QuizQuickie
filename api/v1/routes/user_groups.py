from flask import jsonify, request
from flask_babel import _

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.user_groups import (
    USER_GROUP_GETTER_SCHEMA,
    USER_GROUP_POSTER_SCHEMA,
    USER_GROUP_PUTTER_SCHEMA,
    USER_GROUP_DELETER_SCHEMA,
    USER_GROUP_USERS_GETTER_SCHEMA,
    USER_GROUP_USERS_POSTER_SCHEMA,
    USER_GROUP_USERS_DELETER_SCHEMA,
)


@app_routes.route("/api/v1/user/group", methods=["GET"], strict_slashes=False)
def user_group_getter():
    """GET /api/v1/user/group
    Return:
      - on success: respond with all the user's own groups
      - on error: respond with 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_GROUP_GETTER_SCHEMA
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


@app_routes.route("/api/v1/user/group", methods=["POST"], strict_slashes=False)
def user_group_poster():
    """POST /api/v1/user/group
    Return:
      - on success: create a user group
      - on error: respond with 409 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_GROUP_POSTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [201, err]:  # Stub for 201 response
            return jsonify({}), 201
        case [409, err]:  # Stub for 409 response
            return jsonify({"error": _("duplicate", data=_("title"))}), 409
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/group/<group_id>", methods=["PUT"], strict_slashes=False
)
def user_group_putter(group_id):
    """PUT /api/v1/user/group/<group_id>
    Return:
      - on success: update user group details
      - on error: respond with 404, 409 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_GROUP_PUTTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return jsonify({}), 200
        case [409, err]:  # Stub for 409 response
            return jsonify({"error": _("duplicate", data=_("title"))}), 409
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/group/<group_id>", methods=["DELETE"], strict_slashes=False
)
def user_group_deleter(group_id):
    """DELETE /api/v1/user/group/<group_id>
    Return:
      - on success: delete a user group
      - on error: respond with 404 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_GROUP_DELETER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [204, err]:  # Stub for 204 response
            return jsonify({}), 204
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/group/<group_id>/users", methods=["GET"], strict_slashes=False
)
def user_group_users_getter(group_id):
    """GET /api/v1/user/group/<group_id>/users
    Return:
      - on success: get all the group subscribed users
      - on error: respond with 404, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_GROUP_USERS_GETTER_SCHEMA
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
                                "user_name": "int",
                                "total_score": "int",
                                "attempted_quizzes": [{"quiz_id": "int"}],
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


@app_routes.route(
    "/api/v1/user/group/<group_id>/users", methods=["POST"], strict_slashes=False
)
def user_group_users_poster(group_id):
    """POST /api/v1/user/group/<group_id>/users
    Return:
      - on success: add users to a group
      - on error: respond with 404, 409 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_GROUP_USERS_POSTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [201, err]:  # Stub for 201 response
            return jsonify({}), 201
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        case [409, err]:  # Stub for 409 response
            return jsonify({"error": _("duplicate", data=_("user"))}), 409
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/group/<group_id>/users", methods=["DELETE"], strict_slashes=False
)
def user_group_users_deleter(group_id):
    """DELETE /api/v1/user/group/<group_id>/users
    Return:
      - on success: remove users from group
      - on error: respond with 404, 409 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_GROUP_USERS_DELETER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [204, err]:  # Stub for 204 response
            return jsonify({}), 204
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        case [409, err]:  # Stub for 409 response
            return jsonify({"error": _("duplicate", data=_("user"))}), 409
        case _:
            return jsonify({"error": _("unexpected")}), 500
