from datetime import datetime
from flask import jsonify, request, g, abort
from flask_babel import _
from flasgger import swag_from

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.user_groups import (
    USER_GROUP_GETTER_SCHEMA,
    USER_GROUP_POSTER_SCHEMA,
    USER_GROUP_ONE_GETTER_SCHEMA,
    USER_GROUP_ONE_PUTTER_SCHEMA,
    USER_GROUP_ONE_DELETER_SCHEMA,
    USER_GROUP_ONE_USERS_GETTER_SCHEMA,
    USER_GROUP_ONE_USERS_POSTER_SCHEMA,
    USER_GROUP_ONE_USERS_DELETER_SCHEMA,
)
from models import storage, Group, Ownership, User, Quiz, QuizAttempt, group_user
from models.base import time_fmt
from models.engine.relational_storage import paginate


@app_routes.route("/user/group", methods=["GET"], strict_slashes=False)
@swag_from("documentation/user_groups/user_group_getter.yml")
def user_group_getter():
    """GET /api/v1/user/group
    Return:
      - on success: respond with all the user's own groups
      - on error: respond with 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_GROUP_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        query = (
            storage.query(Group)
            .filter(Group.ownership_id == Ownership.id, Ownership.user_id == user.id)
            .order_by(Group.title.asc())
        )
        try:
            return (
                paginate(
                    "groups",
                    query,
                    req.get("page", None),
                    req.get("page_size", None),
                    apply=lambda group: {"group_id": group.id, "title": group.title},
                ),
                200,
            )
        except ValueError as e:
            data = (
                e.args[0]
                if e.args and e.args[0] in ("page", "page_size")
                else "request"
            )
            return (
                jsonify(
                    {
                        "error": _(
                            "invalid",
                            data=_(data),
                        )
                    }
                ),
                422,
            )
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/user/group", methods=["POST"], strict_slashes=False)
@swag_from("documentation/user_groups/user_group_poster.yml")
def user_group_poster():
    """POST /api/v1/user/group
    Return:
      - on success: create a user group
      - on error: respond with 409 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_GROUP_POSTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        title = req["title"]

        if storage.query(Group).filter_by(title=title).count() > 0:
            return jsonify({"error": _("duplicate", data=_("group"))}), 409
        group_id = (
            storage.new(
                Group(
                    title=title,
                    ownership_id=storage.new(Ownership(user_id=user.id)).save().id,
                )
            )
            .save()
            .id
        )
        return jsonify({"group_id": group_id}), 201
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/user/group/<int:group_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/user_groups/user_group_one_getter.yml")
def user_group_one_getter(group_id):
    """GET /api/v1/user/group/<int:group_id>
    Return:
      - on success: respond with user group details
      - on error: respond with 404, 409 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_GROUP_ONE_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        group: Group = (
            storage.query(Group)
            .filter(
                Group.id == group_id,
                Group.ownership_id == Ownership.id,
                Ownership.user_id == user.id,
            )
            .one_or_none()
        )
        if group is None:
            return jsonify({"error": _("not_found", data=_("group"))}), 404

        return jsonify({"group": {"title": group.title}}), 200
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/user/group/<int:group_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/user_groups/user_group_one_putter.yml")
def user_group_one_putter(group_id):
    """PUT /api/v1/user/group/<int:group_id>
    Return:
      - on success: update user group details
      - on error: respond with 404, 409 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_GROUP_ONE_PUTTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    try:
        group: Group = (
            storage.query(Group)
            .filter(
                Group.id == group_id,
                Group.ownership_id == Ownership.id,
                Ownership.user_id == user.id,
            )
            .one_or_none()
        )
        if group is None:
            return jsonify({"error": _("not_found", data=_("group"))}), 404

        title = req["title"]
        if storage.query(Group).where(Group.title == title).count() > 0:
            return jsonify({"error": _("duplicate", data=_("title"))}), 409

        group.update(title=title)
        return jsonify({}), 200
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/group/<int:group_id>", methods=["DELETE"], strict_slashes=False
)
@swag_from("documentation/user_groups/user_group_one_deleter.yml")
def user_group_one_deleter(group_id):
    """DELETE /api/v1/user/group/<int:group_id>
    Return:
      - on success: delete a user group
      - on error: respond with 404 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_GROUP_ONE_DELETER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    from sqlalchemy import and_

    try:
        group: Group = (
            storage.query(Group)
            .where(
                and_(
                    Group.id == group_id,
                    Group.ownership_id == Ownership.id,
                    Ownership.user_id == user.id,
                )
            )
            .one_or_none()
        )
        if group is None:
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        group.delete()
        return jsonify({}), 204
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/group/<int:group_id>/users", methods=["GET"], strict_slashes=False
)
@swag_from("documentation/user_groups/user_group_one_users_getter.yml")
def user_group_one_users_getter(group_id):
    """GET /api/v1/user/group/<int:group_id>/users
    Return:
      - on success: get all the group subscribed users
      - on error: respond with 404, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_GROUP_ONE_USERS_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    page = int(req["page"]) if req.get("page", None) else None
    page_size = int(req["page_size"]) if req.get("page_size", None) else None
    query = req["query"] if req.get("query", None) else None

    from sqlalchemy import func, distinct, and_

    try:
        group = (
            storage.query(Group)
            .filter(
                Group.ownership_id == Ownership.id,
                Ownership.user_id == user.id,
                Group.id == group_id,
            )
            .one_or_none()
        )
        if group is None:
            return jsonify({"error": _("not_found", data=_("group"))}), 404

        query = (
            storage.query(
                User,
                func.sum(QuizAttempt.score).label("total_score"),
                func.count(distinct(QuizAttempt.quiz_id)).label("attempt_count"),
            )
            .outerjoin(QuizAttempt, User.id == QuizAttempt.user_id)
            .outerjoin(
                Quiz, and_(Quiz.id == QuizAttempt.quiz_id, Quiz.group_id == group_id)
            )
            .join(group_user, and_(group_user.c.user_id == User.id))
            .filter(group_user.c.group_id == group_id)
            .group_by(User.id)
            .order_by(User.user_name)
        )

        try:
            return (
                paginate(
                    "users",
                    query,
                    page,
                    page_size,
                    lambda u: {
                        "user_id": u[0].id,
                        "user_name": u[0].user_name,
                        "total_score": u[1] if u[1] else 0,
                        "attempted_quizzes": u[2],
                    },
                ),
                200,
            )
        except ValueError as e:
            data = (
                e.args[0]
                if e.args and e.args[0] in ("page", "page_size")
                else "request"
            )
            return jsonify({"error": _("invalid", data=_(data))}), 422
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/group/<int:group_id>/users", methods=["POST"], strict_slashes=False
)
@swag_from("documentation/user_groups/user_group_one_users_poster.yml")
def user_group_one_users_poster(group_id):
    """POST /api/v1/user/group/<int:group_id>/users
    Return:
      - on success: add users to a group
      - on error: respond with 404, 409 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_GROUP_ONE_USERS_POSTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    users = req["users"]

    try:
        group: Group = (
            storage.query(Group)
            .filter(
                Group.ownership_id == Ownership.id,
                Ownership.user_id == user.id,
                Group.id == group_id,
            )
            .one_or_none()
        )
        if group is None:
            return jsonify({"error": _("not_found", data=_("group"))}), 404

        for sub in users:
            sub_id = int(sub["user_id"])
            sub: User = storage.query(User).get(sub_id)
            if sub is None:
                return jsonify({"error": _("not_found", data=_("user"))}), 404

            if sub in group.users:
                return jsonify({"error": _("duplicate", data=_("user"))}), 409
            group.users.append(sub)
        storage.save()
        return jsonify({}), 200
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/group/<int:group_id>/users", methods=["DELETE"], strict_slashes=False
)
@swag_from("documentation/user_groups/user_group_one_users_deleter.yml")
def user_group_one_users_deleter(group_id):
    """DELETE /api/v1/user/group/<int:group_id>/users
    Return:
      - on success: remove users from group
      - on error: respond with 404, 409 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_GROUP_ONE_USERS_DELETER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    users = req["users"]

    try:
        group: Group = (
            storage.query(Group)
            .filter(
                Group.ownership_id == Ownership.id,
                Ownership.user_id == user.id,
                Group.id == group_id,
            )
            .one_or_none()
        )
        if group is None:
            return jsonify({"error": _("not_found", data=_("group"))}), 404

        print(group.users)
        print(users)
        for sub in users:
            sub_id = int(sub["user_id"])
            sub: User = storage.query(User).get(sub_id)
            if sub is None or sub not in group.users:
                return jsonify({"error": _("not_found", data=_("user"))}), 404
            group.users.remove(sub)
        print(group.users)
        storage.save()
        return jsonify({}), 204
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)
