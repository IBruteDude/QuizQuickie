from datetime import datetime
from flask import jsonify, request, g, abort
from flask_babel import _
from flasgger import swag_from

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
from models import storage, User, UserSession
from models.base import time_fmt
from models.engine.relational_storage import paginate


@app_routes.route("/auth/signup", methods=["POST"], strict_slashes=False)
@swag_from("documentation/auth/auth_signup_poster.yml")
def auth_signup_poster():
    """POST /api/v1/auth/signup
    Return:
      - on success: create a new user account
      - on error: respond with 400, 409, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = AUTH_SIGNUP_POSTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    from bcrypt import gensalt, hashpw

    try:
        req["password"] = hashpw(req["password"].encode(), gensalt())
        from sqlalchemy import or_

        if (
            storage.query(User)
            .filter(or_(User.email == req["email"], User.user_name == req["user_name"]))
            .count()
            > 0
        ):
            return jsonify({"error": _("duplicate", data=_("email or user name"))}), 409
        user_id = storage.new(User(**req)).save().id
        return jsonify({"user_id": user_id}), 201
    except Exception as e:
        print(e)
        abort(500)


@app_routes.route("/auth/login", methods=["POST"], strict_slashes=False)
@swag_from("documentation/auth/auth_login_poster.yml")
def auth_login_poster():
    """POST /api/v1/auth/login
    Return:
      - on success: create a new session for the user and log in
      - on error: respond with 401 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = AUTH_LOGIN_POSTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    from bcrypt import checkpw
    from api.v1.auth import auth, SessionAuth
    from os import getenv

    try:
        user: User = storage.query(User).where(User.email == req["email"]).one_or_none()
        pass_bytes = req["password"].encode()
        if user is None or not checkpw(pass_bytes, user.password):
            return jsonify({"error": _("invalid", data=_("login details"))}), 401
        resp = jsonify({})
        if isinstance(auth, SessionAuth):
            session_id = auth.create_session(user.id)
            resp.set_cookie(getenv("SESSION_NAME"), session_id)
        return resp, 200
    except Exception as e:
        print(req)
        print(f"{e.__class__.__name__}: {e}")
        abort(500)


@app_routes.route("/auth/password/reset", methods=["GET"], strict_slashes=False)
@swag_from("documentation/auth/auth_password_reset_getter.yml")
def auth_password_reset_getter():
    """GET /api/v1/auth/password/reset
    Return:
      - on success: send a password reset email
      - on error: respond with 401 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = AUTH_PASSWORD_RESET_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        from uuid import uuid4

        user.reset_token = uuid4()
        user.save()
        return jsonify({"reset_token": str(user.reset_token)}), 200
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/auth/password/reset/confirm", methods=["POST"], strict_slashes=False
)
@swag_from("documentation/auth/auth_password_reset_confirm_poster.yml")
def auth_password_reset_confirm_poster():
    """POST /api/v1/auth/password/reset/confirm
    Return:
      - on success: confirm password reset
      - on error: respond with 400 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = AUTH_PASSWORD_RESET_CONFIRM_POSTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    reset_token = req["reset_token"]
    new_password = req["new_password"]

    try:
        from bcrypt import hashpw, gensalt

        if reset_token != str(user.reset_token):
            return jsonify({"error": _("invalid", data=_("token or password"))}), 400
        user.reset_token = None
        user.password = hashpw(new_password.encode(), gensalt())
        user.save()
        return jsonify({}), 200
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/auth/logout", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/auth/auth_logout_deleter.yml")
def auth_logout_deleter():
    """DELETE /api/v1/auth/logout
    Return:
      - on success: remove user session and log out
      - on error: respond with 401 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = AUTH_LOGOUT_DELETER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        from api.v1.auth import auth
        from uuid import UUID

        session_id = auth.session_cookie(request)
        storage.query(UserSession).filter(
            UserSession.uuid == UUID(f"{{{session_id}}}")
        ).delete()
        storage.save()
        return jsonify({}), 204
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/auth/deactivate", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/auth/auth_deactivate_deleter.yml")
def auth_deactivate_deleter():
    """DELETE /api/v1/auth/deactivate
    Return:
      - on success: delete user account
      - on error: respond with 401 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = AUTH_DEACTIVATE_DELETER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        user.delete()
        return jsonify({}), 204
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)
