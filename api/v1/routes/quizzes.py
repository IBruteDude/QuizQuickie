from datetime import datetime
from flask import jsonify, request, g, abort
from flask_babel import _
from flasgger import swag_from

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.quizzes import (
    QUIZ_GETTER_SCHEMA,
    QUIZ_ONE_GETTER_SCHEMA,
    QUIZ_ONE_STATS_GETTER_SCHEMA,
)
from models import storage, Question, Quiz, QuizAttempt, User
from models.base import time_fmt
from models.engine.relational_storage import paginate


@app_routes.route("/quiz", methods=["GET"], strict_slashes=False)
@swag_from("documentation/quizzes/quiz_getter.yml")
def quiz_getter():
    """GET /api/v1/quiz
    Return:
      - on success: respond with quizzes with different filters
      - on error: respond with 404, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = QUIZ_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    category = req.get("category", None)
    difficulty = int(req["difficulty"]) if req.get("difficulty", None) else None
    sort_by = req["sort_by"] if req.get("sort_by", None) else None
    group_id = int(req["group_id"]) if req.get("group_id", None) else None
    page = int(req["page"]) if req.get("page", None) else None
    page_size = int(req["page_size"]) if req.get("page_size", None) else None
    title_query = req["query"] if req.get("query", None) else None

    try:
        query = storage.query(Quiz)

        if group_id:
            query = query.filter(Quiz.group_id == group_id)
        else:
            query = query.filter(Quiz.group_id == None)

        if title_query:
            query = query.filter(Quiz.title.like(f"%{title_query}%"))
        if category:
            query = query.filter(Quiz.category == category)
        if difficulty:
            if not 1 < difficulty < 5:
                return jsonify({"error": _("invalid", data=_("difficulty"))}), 422
            query = query.filter(Quiz.difficulty == difficulty)
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
                    "start": datetime.strftime(q.start, time_fmt),
                    "end": datetime.strftime(q.end, time_fmt),
                    "group_id": q.group_id,
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


@app_routes.route("/quiz/<int:quiz_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/quizzes/quiz_one_getter.yml")
def quiz_one_getter(quiz_id):
    """GET /api/v1/quiz/<int:quiz_id>
    Return:
      - on success: respond with the quiz's list of questions
      - on error: respond with 404, 410 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = QUIZ_ONE_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    try:
        if (
            storage.query(Quiz)
            .filter(Quiz.id == quiz_id, Quiz.group_id == None)
            .one_or_none()
            is None
        ):
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404

        questions = []
        for q in (
            storage.query(Question)
            .where(Question.quiz_id == quiz_id)
            .order_by(Question.order)
            .all()
        ):
            questions.append(
                {
                    "statement": q.statement,
                    "points": q.points,
                    "type": q.type,
                    "options": [ans.text for ans in q.answers],
                }
            )

        return jsonify({"questions": questions}), 200
        # return jsonify({'error': _('deleted', data=_('quiz'))}), 410
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/quiz/<int:quiz_id>/stats", methods=["GET"], strict_slashes=False)
@swag_from("documentation/quizzes/quiz_one_stats_getter.yml")
def quiz_one_stats_getter(quiz_id):
    """GET /api/v1/quiz/<int:quiz_id>/stats
    Return:
      - on success: respond with stats about the user attempts of the quiz
      - on error: respond with 404 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = QUIZ_ONE_STATS_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    from sqlalchemy import func, distinct

    try:
        if (
            storage.query(Quiz)
            .filter(Quiz.id == quiz_id, Quiz.group_id == None)
            .one_or_none()
            is None
        ):
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        stats = storage.query(
            func.max(QuizAttempt.score),
            func.min(QuizAttempt.score),
            func.avg(QuizAttempt.score),
            func.count(distinct(Quiz.user_id)),
        ).where(QuizAttempt.quiz_id == quiz_id)
        return (
            jsonify(
                {
                    "max_score": stats[0],
                    "min_score": stats[1],
                    "average_score": stats[2],
                    "attempts": stats[3],
                }
            ),
            200,
        )
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)
