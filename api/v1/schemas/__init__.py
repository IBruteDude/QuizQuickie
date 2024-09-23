from flask import jsonify
from flask_babel import _
from jsonschema import validate, ValidationError


def json_validate(data, schema):
    try:
        validate(data, schema)
        return None
    except ValidationError as e:
        if "is not of type" in e.message:
            return jsonify({"error": _("invalid", data=e.path[0])}), 422
        elif "Missing required property" in e.message:
            return jsonify({"error": _("missing", data=e.message.split("'")[1])}), 400
        elif "does not match the pattern" in e.message:
            return jsonify({"error": _("invalid", data=e.path[0])}), 422
        return jsonify({"error": _("invalid", data="request")}), 400
