from datetime import datetime
from flask import jsonify, request, g, abort
from flask_babel import _
from flasgger import swag_from

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.user_quizzes import (
    USER_QUIZ_GETTER_SCHEMA,
    USER_QUIZ_POSTER_SCHEMA,
    USER_QUIZ_ONE_GETTER_SCHEMA,
    USER_QUIZ_ONE_PUTTER_SCHEMA,
    USER_QUIZ_ONE_DELETER_SCHEMA,
    USER_QUIZ_ONE_QUESTION_GETTER_SCHEMA,
    USER_QUIZ_ONE_QUESTION_POSTER_SCHEMA,
    USER_QUIZ_ONE_QUESTION_PUTTER_SCHEMA,
    USER_QUIZ_ONE_QUESTION_DELETER_SCHEMA,
    USER_QUIZ_ONE_STATS_ATTEMPTS_GETTER_SCHEMA,
    USER_QUIZ_ONE_STATS_QUESTION_ONE_GETTER_SCHEMA,
)
from models import storage, Group, Question, Quiz, QuizAttempt, User, Ownership, Answer
from models.base import time_fmt
from models.engine.relational_storage import paginate


@app_routes.route("/user/quiz", methods=["GET"], strict_slashes=False)
@swag_from("documentation/user_quizzes/user_quiz_getter.yml")
def user_quiz_getter():
    """GET /api/v1/user/quiz
    Return:
      - on success: respond with the user's created quizzes
      - on error: respond with 404, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_QUIZ_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    title_query = req.get("query", None)
    sort_by = req.get("sort_by", None)
    category = req.get("category", None)
    difficulty = req.get("difficulty", None)

    try:
        query = storage.query(Quiz).where(Quiz.user_id == user.id)
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
                "quizzes", query, req.get("page", None), req.get("page_size", None)
            ),
            200,
        )
    except ValueError as e:
        data = e.args[0] if e.args and e.args[0] in ("page", "page_size") else "request"
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
        # return jsonify({"error": _("not_found", data=_("category"))}), 404
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/user/quiz", methods=["POST"], strict_slashes=False)
@swag_from("documentation/user_quizzes/user_quiz_poster.yml")
def user_quiz_poster():
    """POST /api/v1/user/quiz
    Return:
      - on success: create a new quiz for user
      - on error: respond with 400, 404, 409, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_QUIZ_POSTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    title = req.get("title")
    category = req.get("category")
    difficulty = int(req["difficulty"])
    points = int(req["points"])
    duration = int(req["duration"]) if req.get("duration", None) else None
    start = (
        datetime.strptime(req["start"], time_fmt) if req.get("start", None) else None
    )
    end = datetime.strptime(req["end"], time_fmt) if req.get("end", None) else None
    group_id = int(req["group_id"]) if req.get("group_id", None) else None

    try:
        if difficulty < 0:
            return jsonify({"error": _("invalid", data=_("difficulty"))}), 422
        if points < 0:
            return jsonify({"error": _("invalid", data=_("points"))}), 422
        if duration < 0:
            return jsonify({"error": _("invalid", data=_("duration"))}), 422
        if len({type(start), type(end)}) > 1 or start > end or start < datetime.now():
            return jsonify({"error": _("invalid", data=_("quiz schedule"))}), 422

        if storage.query(Quiz).filter(Quiz.title == title).count() > 0:
            return jsonify({"error": _("duplicate", data=_("title"))}), 409
        if group_id:
            if (
                storage.query(Group)
                .filter(
                    Group.id == group_id,
                    Group.ownership_id == Ownership.id,
                    Ownership.user_id == user.id,
                )
                .one_or_none()
                is None
            ):
                return jsonify({"error": _("not_found", data=_("group"))}), 404

        quiz = Quiz(
            title=title,
            category=category,
            difficulty=difficulty,
            points=points,
            duration=duration,
            start=start,
            end=end,
            user_id=user.id,
            group_id=group_id,
        )
        quiz_id = storage.new(quiz).save().id
        return jsonify({"quiz_id": quiz_id}), 201
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/user/quiz/<int:quiz_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/user_quizzes/user_quiz_one_getter.yml")
def user_quiz_one_getter(quiz_id):
    """GET /api/v1/user/quiz/<int:quiz_id>
    Return:
      - on success: respond with quiz details
      - on error: respond with 404, 409, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_QUIZ_ONE_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        quiz: Quiz = (
            storage.query(Quiz)
            .filter(Quiz.user_id == user.id, Quiz.id == quiz_id)
            .one_or_none()
        )
        if quiz is None:
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        return (
            jsonify(
                {
                    "title": quiz.title,
                    "category": quiz.category,
                    "difficulty": quiz.difficulty,
                    "points": quiz.points,
                    "duration": quiz.duration,
                    "start": datetime.strftime(quiz.start, time_fmt),
                    "end": datetime.strftime(quiz.end, time_fmt),
                    "group_id": quiz.group_id,
                }
            ),
            200,
        )
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/user/quiz/<int:quiz_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/user_quizzes/user_quiz_one_putter.yml")
def user_quiz_one_putter(quiz_id):
    """PUT /api/v1/user/quiz/<int:quiz_id>
    Return:
      - on success: modify the quiz details
      - on error: respond with 404, 409, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_QUIZ_ONE_PUTTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    category = req.get("category", None)
    difficulty = int(req["difficulty"]) if req.get("difficulty", None) else None
    points = int(req["points"]) if req.get("points", None) else None
    duration = int(req["duration"]) if req.get("duration", None) else None
    start = (
        datetime.strptime(req["start"], time_fmt) if req.get("start", None) else None
    )
    end = datetime.strptime(req["end"], time_fmt) if req.get("end", None) else None
    title = req.get("title", None)
    group_id = int(req["group_id"]) if req.get("group_id", None) else None

    try:
        quiz: Quiz = (
            storage.query(Quiz)
            .filter(Quiz.user_id == user.id, Quiz.id == quiz_id)
            .one_or_none()
        )
        if quiz is None:
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404

        if category:
            quiz.category = category

        if difficulty:
            if not 1 <= difficulty <= 5:
                return jsonify({"error": _("invalid", data=_("difficulty"))}), 422
            quiz.difficulty = difficulty

        if points:
            if points < 0:
                return jsonify({"error": _("invalid", data=_("points"))}), 422
            quiz.points = points

        if duration:
            if duration < 0:
                return jsonify({"error": _("invalid", data=_("duration"))}), 422
            quiz.duration = duration
        if start or end:
            if (
                len({type(start), type(end)}) > 1
                or start > end
                or start < datetime.now()
            ):
                return jsonify({"error": _("invalid", data=_("quiz schedule"))}), 422
            quiz.start = start
            quiz.end = end

        if title:
            if storage.query(Quiz).filter_by(title=title).count() > 0:
                return jsonify({"error": _("duplicate", data=_("title"))}), 409
            quiz.title = title

        if group_id:
            if (
                storage.query(Group)
                .filter(
                    Group.id == group_id,
                    Group.ownership_id == Ownership.id,
                    Ownership.user_id == user.id,
                )
                .one_or_none()
                is None
            ):
                return jsonify({"error": _("not_found", data=_("group"))}), 404
            quiz.group_id = group_id
        quiz.save()
        return jsonify({}), 200
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/user/quiz/<int:quiz_id>", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/user_quizzes/user_quiz_one_deleter.yml")
def user_quiz_one_deleter(quiz_id):
    """DELETE /api/v1/user/quiz/<int:quiz_id>
    Return:
      - on success: delete the user's quiz
      - on error: respond with 404 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_QUIZ_ONE_DELETER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        if (
            storage.query(Quiz)
            .where(Quiz.user_id == user.id)
            .where(Quiz.id == quiz_id)
            .one_or_none()
            is None
        ):
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        storage.delete(storage.query(Quiz).get(quiz_id))
        storage.save()
        return jsonify({}), 204
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/quiz/<int:quiz_id>/question", methods=["GET"], strict_slashes=False
)
@swag_from("documentation/user_quizzes/user_quiz_one_question_getter.yml")
def user_quiz_one_question_getter(quiz_id):
    """GET /api/v1/user/quiz/<int:quiz_id>/question
    Return:
      - on success: respond with the quiz's list of questions
      - on error: respond with 404 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_QUIZ_ONE_QUESTION_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        if (
            storage.query(Quiz)
            .where(Quiz.user_id == user.id)
            .where(Quiz.id == quiz_id)
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
                    "correct_answer": [ans.order for ans in q.answers if ans.correct],
                }
            )

        return jsonify({"questions": questions}), 200

    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/quiz/<int:quiz_id>/question", methods=["POST"], strict_slashes=False
)
@swag_from("documentation/user_quizzes/user_quiz_one_question_poster.yml")
def user_quiz_one_question_poster(quiz_id):
    """POST /api/v1/user/quiz/<int:quiz_id>/question
    Return:
      - on success: add questions to the quiz
      - on error: respond with 400, 404, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_QUIZ_ONE_QUESTION_POSTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    questions = req["questions"]

    try:
        if (
            storage.query(Quiz)
            .where(Quiz.user_id == user.id)
            .where(Quiz.id == quiz_id)
            .one_or_none()
            is None
        ):
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404

        question_ids = []
        for i, q in enumerate(questions):
            cor = q["correct_answer"]
            if q["type"] not in ("TFQ", "SCQ", "MCQ"):
                return jsonify({"error": _("invalid", data=_("type"))}), 422
            if (
                (q["type"] in ("TFQ", "SCQ") and len(cor) != 1)
                or (q["type"] == "MCQ" and len(cor) >= len(q["options"]))
                or (q["type"] == "TFQ" and cor[0] > 1)
                or (
                    q["type"] == ("SCQ", "MCQ")
                    and any(a > len(q["options"]) for a in cor)
                )
            ):
                return jsonify({"error": _("invalid", data=_("answer option"))}), 422
            q_id = (
                storage.new(
                    Question(
                        order=i,
                        statement=q["statement"],
                        points=q["points"],
                        type=q["type"],
                        quiz_id=quiz_id,
                    )
                )
                .save()
                .id
            )
            question_ids.append(q_id)
            for i, ans in enumerate(q["options"]):
                storage.new(
                    Answer(
                        text=ans,
                        order=i,
                        correct=(i in q["correct_answer"]),
                        question_id=q_id,
                    )
                ).save()
        return jsonify([{"question_id": q_id} for q_id in question_ids]), 201
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/quiz/<int:quiz_id>/question", methods=["PUT"], strict_slashes=False
)
@swag_from("documentation/user_quizzes/user_quiz_one_question_putter.yml")
def user_quiz_one_question_putter(quiz_id):
    """PUT /api/v1/user/quiz/<int:quiz_id>/question
    Return:
      - on success: modify the quiz's questions
      - on error: respond with 404, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)

    SCHEMA = USER_QUIZ_ONE_QUESTION_PUTTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    questions = req["questions"]

    try:
        if True:  # Stub for 200 response
            return jsonify({}), 200
        if True:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("answer option"))}), 422
        if True:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/quiz/<int:quiz_id>/question", methods=["DELETE"], strict_slashes=False
)
@swag_from("documentation/user_quizzes/user_quiz_one_question_deleter.yml")
def user_quiz_one_question_deleter(quiz_id):
    """DELETE /api/v1/user/quiz/<int:quiz_id>/question
    Return:
      - on success: remove questions from the quiz
      - on error: respond with 404 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_QUIZ_ONE_QUESTION_DELETER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    questions = req["questions"]

    try:
        if True:  # Stub for 204 response
            return jsonify({}), 204
        if True:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/quiz/<int:quiz_id>/stats/attempts", methods=["GET"], strict_slashes=False
)
@swag_from("documentation/user_quizzes/user_quiz_one_stats_attempts_getter.yml")
def user_quiz_one_stats_attempts_getter(quiz_id):
    """GET /api/v1/user/quiz/<int:quiz_id>/stats/attempts
    Return:
      - on success: respond with stats about the user attempts of the quiz
      - on error: respond with 404, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_QUIZ_ONE_STATS_ATTEMPTS_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    page = int(req["page"]) if req.get("page", None) else None
    page_size = int(req["page_size"]) if req.get("page_size", None) else None
    title_query = req["query"] if req.get("query", None) else None

    from sqlalchemy import and_

    try:
        quiz: Quiz = (
            storage.query(Quiz)
            .where(Quiz.user_id == user.id)
            .filter_by(id=quiz_id)
            .one_or_none()
        )
        if quiz is None:
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        query = storage.query(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id)
        if title_query:
            query = query.where(
                and_(
                    QuizAttempt.user_id == User.id,
                    User.user_name.like(f"%{title_query}%"),
                )
            )
        try:
            return (
                paginate(
                    "attempts",
                    query,
                    page,
                    page_size,
                    apply=lambda a: {
                        "user_id": a.user.id,
                        "user_name": a.user.user_name,
                        "attempt_id": a.id,
                        "time": a.created_at,
                        "points": a.score,
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
    "/user/quiz/<int:quiz_id>/stats/question/<int:question_id>",
    methods=["GET"],
    strict_slashes=False,
)
@swag_from("documentation/user_quizzes/user_quiz_one_stats_question_one_getter.yml")
def user_quiz_one_stats_question_one_getter(quiz_id, question_id):
    """GET /api/v1/user/quiz/<int:quiz_id>/stats/question/<int:question_id>
    Return:
      - on success: respond with stats about the user attempts of a quiz's question
      - on error: respond with 404, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_QUIZ_ONE_STATS_QUESTION_ONE_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    page = int(req["page"]) if req.get("page", None) else None
    page_size = int(req["page_size"]) if req.get("page_size", None) else None
    query = req["query"] if req.get("query", None) else None

    try:
        if True:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "total_pages": "int",
                        "total_question_answers": "int",
                        "next": "int",
                        "prev": "int",
                        "question_answers": [
                            {"correct_answers": "int", "wrong_answers": ["int"]}
                        ],
                    }
                ),
                200,
            )
        if True:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        if True:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422

        query = storage.query()
        try:
            return (
                paginate(
                    "question_answers",
                    query,
                    req.get("page", None),
                    req.get("page_size", None),
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
