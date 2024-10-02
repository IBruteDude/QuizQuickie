from datetime import datetime
from flask import jsonify, request, g, abort
from flask_babel import _
from flasgger import swag_from

from api.v1.routes import app_routes
from models import storage, User, Group, Ownership, Quiz
from models.base import time_fmt
from models.engine.relational_storage import paginate
from bcrypt import gensalt, hashpw


@app_routes.route("/test/<command>", methods=["POST"], strict_slashes=False)
def test_command(command):
    r = request.json
    match command:
        case "reload":
            storage.reload()
            return jsonify({}), 200
        case "users":
            user_ids = []
            for req in r:
                req["password"] = hashpw(req["password"].encode(), gensalt())
                from sqlalchemy import or_

                if (
                    storage.query(User)
                    .where(
                        or_(
                            User.email == req["email"],
                            User.user_name == req["user_name"],
                        )
                    )
                    .count()
                    > 0
                ):
                    return (
                        jsonify(
                            {"error": _("duplicate", data=_("email or user name"))}
                        ),
                        409,
                    )
                user_ids.append({"user_id": storage.new(User(**req)).save().id})
            return jsonify(user_ids), 201
        case "groups":
            group_ids = []
            user_id = r["user_id"]
            r = r["body"]
            for req in r:
                title = req["title"]

                if storage.query(Group).filter_by(title=title).count() > 0:
                    return jsonify({"error": _("duplicate", data=_("group"))}), 409
                group_ids.append(
                    {
                        "group_id": storage.new(
                            Group(
                                title=title,
                                ownership_id=storage.new(Ownership(user_id=user_id))
                                .save()
                                .id,
                            )
                        )
                        .save()
                        .id
                    }
                )
            return jsonify(group_ids), 201

        case "quizzes":
            quiz_ids = []
            user_id = r["user_id"]
            r = r["body"]
            for req in r:
                title = req["title"]
                category = req["category"]
                difficulty = int(req["difficulty"])
                points = int(req["points"])
                duration = int(req["duration"]) if req.get("duration", None) else None
                start = (
                    datetime.strptime(req["start"], time_fmt)
                    if req.get("start", None)
                    else None
                )
                end = (
                    datetime.strptime(req["end"], time_fmt)
                    if req.get("end", None)
                    else None
                )
                group_id = int(req["group_id"]) if req.get("group_id", None) else None

                if difficulty < 0:
                    return jsonify({"error": _("invalid", data=_("difficulty"))}), 422
                if points < 0:
                    return jsonify({"error": _("invalid", data=_("points"))}), 422
                if duration < 0:
                    return jsonify({"error": _("invalid", data=_("duration"))}), 422
                if (
                    len({type(start), type(end)}) > 1
                    or start > end
                    or start < datetime.now()
                ):
                    return (
                        jsonify({"error": _("invalid", data=_("quiz schedule"))}),
                        422,
                    )

                if storage.query(Quiz).where(Quiz.title == title).count() > 0:
                    return jsonify({"error": _("duplicate", data=_("title"))}), 409
                if group_id:
                    if (
                        storage.query(Group)
                        .filter(
                            Group.id == group_id,
                            Group.ownership_id == Ownership.id,
                            Ownership.user_id == user_id,
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
                    user_id=user_id,
                    group_id=group_id,
                )
                quiz_ids.append({"quiz_id": storage.new(quiz).save().id})
            return jsonify(quiz_ids), 201

        case "sub_groups":
            user_id = int(r["user_id"])
            user: User = storage.query(User).get(user_id)

            r = r["body"]
            for req in r:
                group_id = int(req["id"])
                group: Group = storage.query(Group).get(group_id)
                group.users.append(user)
                storage.save()
            return jsonify({}), 200

        case "unsub_groups":
            user_id = int(r["user_id"])
            user: User = storage.query(User).get(user_id)

            r = r["body"]
            for req in r:
                group_id = int(req["id"])
                group: Group = storage.query(Group).get(group_id)
                group.users.remove(user)
                storage.save()
            return jsonify({}), 204
        case "add_quizzes":
            user_id = int(r["user_id"])
            group_id = int(r["group_id"])
            user: User = storage.query(User).get(user_id)

            r = r["body"]
            for req in r:
                quiz_id = int(req["quiz_id"])
                quiz: Quiz = (
                    storage.query(Quiz)
                    .filter(Quiz.user_id == user.id, Quiz.id == quiz_id)
                    .one_or_none()
                )
                quiz.group_id = group_id
            storage.save()
            return jsonify({}), 200
