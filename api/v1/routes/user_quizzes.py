from flask import jsonify, request
from flask_babel import _

from api.v1.routes import app_routes
from api.v1.schemas import json_validate
from api.v1.schemas.user_quizzes import (
    USER_QUIZ_GETTER_SCHEMA,
    USER_QUIZ_POSTER_SCHEMA,
    USER_QUIZ_PUTTER_SCHEMA,
    USER_QUIZ_DELETER_SCHEMA,
    USER_QUIZ_QUESTION_GETTER_SCHEMA,
    USER_QUIZ_QUESTION_POSTER_SCHEMA,
    USER_QUIZ_QUESTION_PUTTER_SCHEMA,
    USER_QUIZ_QUESTION_DELETER_SCHEMA,
    USER_QUIZ_STATS_ATTEMPTS_GETTER_SCHEMA,
    USER_QUIZ_STATS_QUESTION_GETTER_SCHEMA,
)


@app_routes.route("/api/v1/user/quiz", methods=["GET"], strict_slashes=False)
def user_quiz_getter():
    """GET /api/v1/user/quiz
    Return:
      - on success: respond with the user's created quizzes
      - on error: respond with 404, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_QUIZ_GETTER_SCHEMA
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
                                "category": "str",
                                "difficulty": "int",
                                "points": "int",
                                "duration": "int",
                            }
                        ],
                    }
                ),
                200,
            )
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("category"))}), 404
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/user/quiz", methods=["POST"], strict_slashes=False)
def user_quiz_poster():
    """POST /api/v1/user/quiz
    Return:
      - on success: create a new quiz for user
      - on error: respond with 400, 404, 409, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_QUIZ_POSTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [201, err]:  # Stub for 201 response
            return jsonify({}), 201
        case [400, err]:  # Stub for 400 response
            return jsonify({"error": _("incomplete", data=_("quiz"))}), 400
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("group"))}), 404
        case [409, err]:  # Stub for 409 response
            return jsonify({"error": _("duplicate", data=_("title"))}), 409
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("quiz schedule"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route("/api/v1/user/quiz/<quiz_id>", methods=["PUT"], strict_slashes=False)
def user_quiz_putter(quiz_id):
    """PUT /api/v1/user/quiz/<quiz_id>
    Return:
      - on success: modify the quiz details
      - on error: respond with 404, 409, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_QUIZ_PUTTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return jsonify({}), 200
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case [409, err]:  # Stub for 409 response
            return jsonify({"error": _("duplicate", data=_("title"))}), 409
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("quiz schedule"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/quiz/<quiz_id>", methods=["DELETE"], strict_slashes=False
)
def user_quiz_deleter(quiz_id):
    """DELETE /api/v1/user/quiz/<quiz_id>
    Return:
      - on success: delete the user's quiz
      - on error: respond with 404 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_QUIZ_DELETER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [204, err]:  # Stub for 204 response
            return jsonify({}), 204
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/quiz/<quiz_id>/question", methods=["GET"], strict_slashes=False
)
def user_quiz_question_getter(quiz_id):
    """GET /api/v1/user/quiz/<quiz_id>/question
    Return:
      - on success: respond with the quiz's list of questions
      - on error: respond with 404 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_QUIZ_QUESTION_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "questions": [
                            {
                                "statement": "str",
                                "points": "int",
                                "type": "str",
                                "options": ["str"],
                                "correct_answer": ["int"],
                            }
                        ]
                    }
                ),
                200,
            )
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/quiz/<quiz_id>/question", methods=["POST"], strict_slashes=False
)
def user_quiz_question_poster(quiz_id):
    """POST /api/v1/user/quiz/<quiz_id>/question
    Return:
      - on success: add questions to the quiz
      - on error: respond with 400, 404, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_QUIZ_QUESTION_POSTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [201, err]:  # Stub for 201 response
            return jsonify({}), 201
        case [400, err]:  # Stub for 400 response
            return jsonify({"error": _("missing", data=_("answers"))}), 400
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("answer option"))}), 422
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/quiz/<quiz_id>/question", methods=["PUT"], strict_slashes=False
)
def user_quiz_question_putter(quiz_id):
    """PUT /api/v1/user/quiz/<quiz_id>/question
    Return:
      - on success: modify the quiz's questions
      - on error: respond with 404, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_QUIZ_QUESTION_PUTTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {"success": _("success", action=_("update"), data=_("question"))}
                ),
                200,
            )
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("answer option"))}), 422
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/quiz/<quiz_id>/question", methods=["DELETE"], strict_slashes=False
)
def user_quiz_question_deleter(quiz_id):
    """DELETE /api/v1/user/quiz/<quiz_id>/question
    Return:
      - on success: remove questions from the quiz
      - on error: respond with 404 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_QUIZ_QUESTION_DELETER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [204, err]:  # Stub for 204 response
            return jsonify({}), 204
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/quiz/<quiz_id>/stats/attempts", methods=["GET"], strict_slashes=False
)
def user_quiz_stats_attempts_getter(quiz_id):
    """GET /api/v1/user/quiz/<quiz_id>/stats/attempts
    Return:
      - on success: respond with stats about the user attempts of the quiz
      - on error: respond with 404, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_QUIZ_STATS_ATTEMPTS_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
            return (
                jsonify(
                    {
                        "total_pages": "int",
                        "total_attempts": "int",
                        "next": "int",
                        "prev": "int",
                        "attempts": [
                            {
                                "user_id": "int",
                                "user_name": "str",
                                "attempt_id": "int",
                                "time": "datetime",
                                "points": "int",
                            }
                        ],
                    }
                ),
                200,
            )
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500


@app_routes.route(
    "/api/v1/user/quiz/<quiz_id>/stats/question/<question_id>",
    methods=["GET"],
    strict_slashes=False,
)
def user_quiz_stats_question_getter(quiz_id, question_id):
    """GET /api/v1/user/quiz/<quiz_id>/stats/question/<question_id>
    Return:
      - on success: respond with stats about the user attempts of a quiz's question
      - on error: respond with 404, 422 error codes
    """
    data = request.args
    if request.content_type == "application/json":
        data.update(request.json)
    status, err = 0, None

    SCHEMA = USER_QUIZ_STATS_QUESTION_GETTER_SCHEMA
    error_response = json_validate(data, SCHEMA)
    if error_response is not None:
        return error_response

    match [status, err]:
        case [200, err]:  # Stub for 200 response
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
        case [404, err]:  # Stub for 404 response
            return jsonify({"error": _("not_found", data=_("quiz"))}), 404
        case [422, err]:  # Stub for 422 response
            return jsonify({"error": _("invalid", data=_("page_size"))}), 422
        case _:
            return jsonify({"error": _("unexpected")}), 500
