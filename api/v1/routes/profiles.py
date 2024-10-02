from datetime import datetime
from flask import jsonify, request, g, abort
from flask_babel import _
from flasgger import swag_from

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.profiles import (
    PROFILE_GETTER_SCHEMA,
    PROFILE_ONE_GETTER_SCHEMA,
    PROFILE_ONE_QUIZ_GETTER_SCHEMA,
)
from models import storage, Group, Ownership, Quiz, QuizAttempt, User, group_user
from models.base import time_fmt
from models.engine.relational_storage import paginate


@app_routes.route("/profile", methods=["GET"], strict_slashes=False)
@swag_from("documentation/profiles/profile_getter.yml")
def profile_getter():
    """GET /api/v1/profile
    Return:
      - on success: respond with user profile info
      - on error: respond with 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = PROFILE_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    page = int(req["page"]) if req.get("page", None) else None
    page_size = int(req["page_size"]) if req.get("page_size", None) else None
    username_query = req.get("query", None)

    try:
        query = storage.query(User.id, User.user_name).order_by(User.user_name.asc())

        if username_query:
            query = query.filter(User.user_name.like(f"%{username_query}%"))

        return (
            paginate(
                "users",
                query,
                page,
                page_size,
                lambda u: {"user_id": u[0], "user_name": u[1]},
            ),
            200,
        )
    except ValueError as e:
        data = e.args[0] if e.args and e.args[0] in ("page", "page_size") else "request"
        return jsonify({"error": _("invalid", data=_(data))}), 422
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/profile/<int:user_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/profiles/profile_one_getter.yml")
def profile_one_getter(user_id):
    """GET /api/v1/profile/<int:user_id>
    Return:
      - on success: respond with user profile info
      - on error: respond with 404 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = PROFILE_ONE_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    try:
        from sqlalchemy import func, and_, label

        user: User = storage.query(User).where(User.id == user_id).one_or_none()
        if user is None:
            return jsonify({"error": _("not_found", data=_("user"))}), 404
        u_data = storage.query(
            func.count(Ownership),
            func.count(Quiz),
            func.count(group_user.c.group_id),
            func.count(QuizAttempt),
        ).filter(
            Ownership.user_id == user_id,
            Quiz.user_id == user_id,
            group_user.c.user_id == user_id,
            QuizAttempt.user_id == user_id,
            QuizAttempt.score == func.sum(Quiz.questions.points),
        )
        return (
            jsonify(
                {
                    "user_name": user.user_name,
                    "owned_groups": u_data[0],
                    "created_quizzes": u_data[1],
                    "subscribed_groups": u_data[2],
                    "solved_quizzes": u_data[3],
                }
            ),
            200,
        )
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/profile/<int:user_id>/quiz", methods=["GET"], strict_slashes=False)
@swag_from("documentation/profiles/profile_one_quiz_getter.yml")
def profile_one_quiz_getter(user_id):
    """GET /api/v1/profile/<int:user_id>/quiz
    Return:
      - on success: respond with the user's created quizzes
      - on error: respond with 404, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = PROFILE_ONE_QUIZ_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    category = req["category"] if req.get("category", None) else None
    sort_by = req["sort_by"] if req.get("sort_by", None) else None
    difficulty = int(req["difficulty"]) if req.get("difficulty", None) else None
    page = int(req["page"]) if req.get("page", None) else None
    page_size = int(req["page_size"]) if req.get("page_size", None) else None
    title_query = req["query"] if req.get("query", None) else None

    try:
        owner = storage.query(User).get(user_id)
        if owner is None:
            return jsonify({"error": _("not_found", data=_("user"))}), 404

        query = storage.query(Quiz).filter(Quiz.user_id == user_id)
        if title_query:
            query = query.where(Quiz.title.like(f"%{title_query}%"))
        if difficulty:
            query = query.where(Quiz.difficulty == difficulty)
        if category:
            query = query.where(Quiz.category == category)
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

        return (
            paginate(
                "quizzes",
                query,
                page,
                page_size,
                lambda q: {
                    "quiz_id": q.id,
                    "title": q.title,
                    "category": q.category,
                    "difficulty": q.difficulty,
                    "points": q.points,
                    "duration": q.duration,
                },
            ),
            200,
        )
        # return jsonify({'error': _('not_found', data=_('category'))}), 404
    except ValueError as e:
        data = e.args[0] if e.args and e.args[0] in ("page", "page_size") else "request"
        return jsonify({"error": _("invalid", data=_(data))}), 422
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)
