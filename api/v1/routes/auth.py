from flask import jsonify, request
from flask_babel import _

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.auth import (
    AUTH_SIGNUP_POSTER_SCHEMA,
    AUTH_LOGIN_POSTER_SCHEMA,
    AUTH_PASSWORD_RESET_GETTER_SCHEMA,
    AUTH_PASSWORD_RESET_CONFIRM_POSTER_SCHEMA,
    AUTH_LOGOUT_DELETER_SCHEMA,
    AUTH_DEACTIVATE_DELETER_SCHEMA,
)


@app_routes.route("/api/v1/auth/signup", methods=["POST"], strict_slashes=False)
def auth_signup_poster():
    """POST /api/v1/auth/signup
    Return:
      - on success: create a new user account
      - on error: respond with 400, 409, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = AUTH_SIGNUP_POSTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    data[""]

    match [status, err]:
        case [201, err]:  # Stub for 201 response
            return jsonify({}), 201
        case [409, err]:  # Stub for 409 response
            return jsonify({"error": _("duplicate", data=_("user_name"))}), 409
        case [400, err]:  # Stub for 400 response
            return jsonify({"error": _("incomplete", data=_("login details"))}), 400
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("login details"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/auth/login", methods=["POST"], strict_slashes=False)
def auth_login_poster():
    """POST /api/v1/auth/login
    Return:
      - on success: create a new session for the user and log in
      - on error: respond with 401 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = AUTH_LOGIN_POSTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return jsonify({}), 200
        case [401, err]:  # Stub for 401 response
            return jsonify({"error": _("invalid", data=_("login details"))}), 401
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/auth/password/reset", methods=["GET"], strict_slashes=False)
def auth_password_reset_getter():
    """GET /api/v1/auth/password/reset
    Return:
      - on success: send a password reset email
      - on error: respond with 401 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = AUTH_PASSWORD_RESET_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return jsonify({}), 200
        case [401, err]:  # Stub for 401 response
            return jsonify({"error": _("unauthorized")}), 401
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/auth/password/reset/confirm", methods=["POST"], strict_slashes=False
)
def auth_password_reset_confirm_poster():
    """POST /api/v1/auth/password/reset/confirm
    Return:
      - on success: confirm password reset
      - on error: respond with 400 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = AUTH_PASSWORD_RESET_CONFIRM_POSTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return jsonify({}), 200
        case [400, err]:  # Stub for 400 response
            return jsonify({"error": _("invalid", data=_("token or password"))}), 400
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/auth/logout", methods=["DELETE"], strict_slashes=False)
def auth_logout_deleter():
    """DELETE /api/v1/auth/logout
    Return:
      - on success: remove user session and log out
      - on error: respond with 401 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = AUTH_LOGOUT_DELETER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [204, err]:  # Stub for 204 response
            return jsonify({}), 204
        case [401, err]:  # Stub for 401 response
            return jsonify({"error": _("unauthorized")}), 401
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/auth/deactivate", methods=["DELETE"], strict_slashes=False)
def auth_deactivate_deleter():
    """DELETE /api/v1/auth/deactivate
    Return:
      - on success: delete user account
      - on error: respond with 401 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = AUTH_DEACTIVATE_DELETER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [204, err]:  # Stub for 204 response
            return jsonify({}), 204
        case [401, err]:  # Stub for 401 response
            return jsonify({"error": _("unauthorized")}), 401
        case _:
            return jsonify({"error": _("unexpected")}), 500
