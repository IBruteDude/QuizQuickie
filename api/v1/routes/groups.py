from datetime import datetime
from flask import jsonify, request, g, abort
from flask_babel import _
from flasgger import swag_from

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.groups import (
    GROUP_GETTER_SCHEMA,
    GROUP_ONE_USERS_GETTER_SCHEMA,
    GROUP_ONE_QUIZZES_GETTER_SCHEMA,
)
from models import storage, Group, QuizAttempt, Quiz, User
from models.base import time_fmt
from models.engine.relational_storage import paginate


@app_routes.route("/group", methods=["GET"], strict_slashes=False)
@swag_from("documentation/groups/group_getter.yml")
def group_getter():
    """GET /api/v1/group
    Return:
      - on success: respond with a list of available user groups
      - on error: respond with 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = GROUP_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    page = int(req["page"]) if req.get("page", None) else None
    page_size = int(req["page_size"]) if req.get("page_size", None) else None
    title_query = req["query"] if req.get("query", None) else None

    try:
        query = storage.query(Group)
        if title_query:
            query = query.where(Group.title.like(f"%{title_query}%"))
        try:
            return (
                paginate(
                    "groups",
                    query,
                    page,
                    page_size,
                    apply=lambda group: {
                        "group_id": group.id,
                        "title": group.title,
                        "owner_id": group.ownership.user_id,
                        "owner_name": group.ownership.user.user_name,
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


@app_routes.route("/group/<int:group_id>/users", methods=["GET"], strict_slashes=False)
@swag_from("documentation/groups/group_one_users_getter.yml")
def group_one_users_getter(group_id):
    """GET /api/v1/group/<int:group_id>/users
    Return:
      - on success: respond with a list of the groups subscribed users
      - on error: respond with 403, 404, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = GROUP_ONE_USERS_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    sort_by = req["sort_by"] if req.get("sort_by", None) else None
    status = req["status"] if req.get("status", None) else None
    max_score = int(req["max_score"]) if req.get("max_score", None) else None
    min_score = int(req["min_score"]) if req.get("min_score", None) else None
    page = int(req["page"]) if req.get("page", None) else None
    page_size = int(req["page_size"]) if req.get("page_size", None) else None
    username_query = req["query"] if req.get("query", None) else None

    from sqlalchemy import func, and_

    try:
        group = storage.query(Group).get(group_id)
        if group is None:
            return jsonify({"error": _("not_found", data=_("group"))}), 404

        # return jsonify({'error': _('unauthorized')}), 403
        query = (
            storage.query(User, func.sum(QuizAttempt.score))
            .join(
                QuizAttempt, User.id == QuizAttempt.user_id
            )  # Join User with QuizAttempt
            .join(Quiz, QuizAttempt.quiz_id == Quiz.id)  # Join QuizAttempt with Quiz
            .where(Quiz.group_id == group_id)  # Filter by the Quiz group ID
            .group_by(User.id)  # Group by User ID
        )
        filters = []
        if username_query:
            filters.append(
                User.user_name.like(f"%{username_query}%")
            )  # Filter users by username
        if min_score:
            filters.append(func.sum(QuizAttempt.score) >= min_score)
        if max_score:
            filters.append(func.sum(QuizAttempt.score) <= max_score)
        if status:
            filters.append(func.count(User.user_sessions) > 0)
        query = query.having(*filters)
        if sort_by:
            if sort_by == "score":
                query = query.order_by(func.sum(QuizAttempt.score).desc())
            if sort_by == "user_name":
                query = query.order_by(User.user_name.asc())
        try:
            return (
                paginate(
                    "users",
                    query,
                    page,
                    page_size,
                    apply=lambda u: {
                        "user_id": u[0].id,
                        "user_name": u[0].user_name,
                        "status": "active" if len(u[0].user_sessions) > 0 else "away",
                        "score": u[1],
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
    "/group/<int:group_id>/quizzes", methods=["GET"], strict_slashes=False
)
@swag_from("documentation/groups/group_one_quizzes_getter.yml")
def group_one_quizzes_getter(group_id):
    """GET /api/v1/group/<int:group_id>/quizzes
    Return:
      - on success: respond with all the schedualed quizzes
      - on error: respond with 404, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = GROUP_ONE_QUIZZES_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    category = req.get("category", None)
    difficulty = int(req["difficulty"]) if req.get("difficulty", None) else None

    try:
        if storage.query(Group).get(group_id) is None:
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        query = storage.query(Quiz).where(Quiz.group_id == group_id)

        sort_by = req.get("sort_by", None)
        if sort_by in (
            "title",
            "category",
            "difficulty",
            "points",
            "duration",
            "start",
            "end",
        ):
            query = query.order_by(getattr(Quiz, sort_by))
        else:
            query = query.order_by(Quiz.title)
        if category:
            query = query.filter(Quiz.category == category)
        if difficulty:
            if not 1 < difficulty < 5:
                return jsonify({"error": _("invalid", data=_("difficulty"))}), 422
            query = query.filter(Quiz.difficulty == difficulty)

        try:
            return (
                paginate(
                    "quizzes",
                    query,
                    req.get("page", None),
                    req.get("page_size", None),
                    lambda q: {
                        "quiz_id": q.id,
                        "title": q.title,
                        "start": datetime.strftime(q.start, time_fmt),
                        "end": datetime.strftime(q.end, time_fmt),
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
