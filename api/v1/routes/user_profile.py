from datetime import datetime, timezone
from flask import jsonify, request, g, abort
from flask_babel import _
from flasgger import swag_from

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.user_profile import (
    USER_PROFILE_GETTER_SCHEMA,
    USER_PROFILE_PUTTER_SCHEMA,
    USER_PROFILE_QUIZ_ONE_ATTEMPTS_GETTER_SCHEMA,
    USER_PROFILE_QUIZ_ONE_ATTEMPTS_POSTER_SCHEMA,
    USER_PROFILE_GROUP_GETTER_SCHEMA,
    USER_PROFILE_GROUP_POSTER_SCHEMA,
    USER_PROFILE_GROUP_ONE_DELETER_SCHEMA,
)
from models import (
    storage,
    Group,
    Quiz,
    User,
    QuizAttempt,
    Question,
    Answer,
    UserAnswer,
    group_user,
    Ownership,
)
from models.base import time_fmt
from models.engine.relational_storage import paginate


@app_routes.route("/user/profile", methods=["GET"], strict_slashes=False)
@swag_from("documentation/user_profile/user_profile_getter.yml")
def user_profile_getter():
    """GET /api/v1/user/profile
    Return:
      - on success: respond with user profile details
      - on error: respond with  error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_PROFILE_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        return (
            jsonify(
                {
                    "user": {
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "user_name": user.user_name,
                        "profile_picture": user.profile_picture,
                    }
                }
            ),
            200,
        )
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/user/profile", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/user_profile/user_profile_putter.yml")
def user_profile_putter():
    """PUT /api/v1/user/profile
    Return:
      - on success: change user profile details
      - on error: respond with 400, 409 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_PROFILE_PUTTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    first_name = req["first_name"] if req.get("first_name", None) else None
    last_name = req["last_name"] if req.get("last_name", None) else None
    user_name = req["user_name"] if req.get("user_name", None) else None
    profile_picture = (
        req["profile_picture"] if req.get("profile_picture", None) else None
    )

    try:
        if user_name:
            if storage.query(User).where(User.user_name == user_name).count() > 0:
                return jsonify({"error": _("duplicate", data=_("user_name"))}), 409
            user.user_name = user_name
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if profile_picture:
            user.profile_picture = profile_picture
        user.save()
        return jsonify({}), 200
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/profile/quiz/<int:quiz_id>/attempts", methods=["GET"], strict_slashes=False
)
@swag_from("documentation/user_profile/user_profile_quiz_one_attempts_getter.yml")
def user_profile_quiz_one_attempts_getter(quiz_id):
    """GET /api/v1/user/profile/quiz/<int:quiz_id>/attempts
    Return:
      - on success: respond with all user's quiz attempts
      - on error: respond with 403, 404, 410, 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_PROFILE_QUIZ_ONE_ATTEMPTS_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    page = int(req["page"]) if req.get("page", None) else None
    page_size = int(req["page_size"]) if req.get("page_size", None) else None
    quiz_query = req["query"] if req.get("query", None) else None

    from sqlalchemy import and_

    try:
        if (
            storage.query(Quiz)
            .join(QuizAttempt, QuizAttempt.quiz_id == Quiz.id)
            .where(and_(QuizAttempt.user_id == user.id, Quiz.id == quiz_id))
            .one_or_none()
            is None
        ):
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404

        if storage.query(Quiz).get(quiz_id).end < datetime.now():
            return jsonify({"error": _("quiz time has ended")}), 403

        query = storage.query(QuizAttempt).filter_by(quiz_id=quiz_id, user_id=user.id)

        if quiz_query:
            query = query.join(Quiz, QuizAttempt.quiz_id == Quiz.id).where(
                Quiz.title.like(f"%{quiz_query}%")
            )

        try:
            return (
                paginate(
                    "attempts",
                    query,
                    page,
                    page_size,
                    lambda a: {
                        "attempt_id": a.id,
                        "time": datetime.strftime(a.created_at, time_fmt),
                        "score": a.score,
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
    "/user/profile/quiz/<int:quiz_id>/attempts", methods=["POST"], strict_slashes=False
)
@swag_from("documentation/user_profile/user_profile_quiz_one_attempts_poster.yml")
def user_profile_quiz_one_attempts_poster(quiz_id):
    """POST /api/v1/user/profile/quiz/<int:quiz_id>/attempts
    Return:
      - on success: submit user answers for the quiz's questions
      - on error: respond with 404 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_PROFILE_QUIZ_ONE_ATTEMPTS_POSTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    answers = req["answers"]

    try:
        quiz = storage.query(Quiz).get(quiz_id)

        if quiz is None:
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404

        if len(answers) != len(quiz.questions):
            return jsonify({"error": _("invalid", data=_("answer option"))}), 404

        attempt = storage.new(QuizAttempt(score=0, quiz_id=quiz_id, user_id=user.id))

        total_score = 0
        full_score = True
        correct_answers = []
        for ans, q in zip(answers, quiz.questions):
            for a in ans["options"]:
                storage.new(
                    UserAnswer(attempt_id=attempt.id, answer=a, question_id=q.id)
                ).save()
            correct_answer = set(a.order for a in q.answers if a.correct)
            if correct_answer == set(ans["options"]):
                total_score += q.points
            else:
                full_score = False
            correct_answers.append({"options": list(correct_answer)})

        attempt.score = total_score
        attempt.full_score = full_score
        attempt.save()

        return (
            jsonify({"score": total_score, "correct_answers": correct_answers}),
            200,
        )
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/user/profile/group", methods=["GET"], strict_slashes=False)
@swag_from("documentation/user_profile/user_profile_group_getter.yml")
def user_profile_group_getter():
    """GET /api/v1/user/profile/group
    Return:
      - on success: respond with all the user's subscribed groups
      - on error: respond with 422 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_PROFILE_GROUP_GETTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    page = int(req["page"]) if req.get("page", None) else None
    page_size = int(req["page_size"]) if req.get("page_size", None) else None
    title_query = req["query"] if req.get("query", None) else None

    try:
        query = (
            storage.query(Group)
            .join(group_user, Group.id == group_user.c.group_id)
            .filter(group_user.c.user_id == user.id)
            .order_by(Group.title)
        )
        return (
            paginate(
                "groups",
                query,
                page,
                page_size,
                apply=lambda g: {"group_id": g.id, "group_title": g.title},
            ),
            200,
        )
    except ValueError as e:
        data = e.args[0] if e.args and e.args[0] in ("page", "page_size") else "request"
        return jsonify({"error": _("invalid", data=_(data))}), 422
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route("/user/profile/group", methods=["POST"], strict_slashes=False)
@swag_from("documentation/user_profile/user_profile_group_poster.yml")
def user_profile_group_poster():
    """POST /api/v1/user/profile/group
    Return:
      - on success: subscribe the user to the group
      - on error: respond with 404, 409, 410 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_PROFILE_GROUP_POSTER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401
    group_id = int(req["group_id"])

    try:
        group: Group = storage.query(Group).get(group_id)
        if group is None:
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        if user in group.users:
            return jsonify({"error": _("already subscribed to group")}), 409
        group.users.append(user)
        storage.save()
        return jsonify({}), 200
        # return jsonify({"error": _("deleted", data=_("group"))}), 410
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)


@app_routes.route(
    "/user/profile/group/<int:group_id>", methods=["DELETE"], strict_slashes=False
)
@swag_from("documentation/user_profile/user_profile_group_one_deleter.yml")
def user_profile_group_one_deleter(group_id):
    """DELETE /api/v1/user/profile/group/<int:group_id>
    Return:
      - on success: unsubscribe user from a group
      - on error: respond with 404, 409, 410 error codes
    """
    req = dict(request.args)
    if request.content_type == "application/json":
        req.update(request.json)
    SCHEMA = USER_PROFILE_GROUP_ONE_DELETER_SCHEMA
    error_response = json_validate(req, SCHEMA)
    if error_response is not None:
        return error_response

    user: User = getattr(g, "user", None)
    if user is None:
        return jsonify({"error": _("unauthorized")}), 401

    try:
        group: Group = storage.query(Group).get(group_id)
        if group is None:
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        if user not in group.users:
            return jsonify({"error": _("user not subscribed to group")}), 409
        subscription = storage.query(group_user).filter_by(
            group_id=group_id, user_id=user.id
        )
        subscription.delete()
        storage.save()
        return jsonify({}), 204
        # return jsonify({"error": _("deleted", data=_("group"))}), 410
    except Exception as e:
        print(f"[{e.__class__.__name__}]: {e}")
        abort(500)
