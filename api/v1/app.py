#!/usr/bin/env python3
"""Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, request, make_response
from flask_cors import CORS
from flask_babel import Babel, _
from flasgger import Swagger
from api.v1.routes import app_routes
from api.v1.auth import auth
from config import Config
from models import storage


app = Flask(__name__)
app.register_blueprint(app_routes)
app.config.from_object(Config)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
Swagger(app)


def get_locale():
    """get the best matching locale from configured languages"""
    if request.args.get("lang", None) in app.config["LANGUAGES"]:
        return request.args["lang"]
    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_timezone():
    """"""


Babel(
    app,
    locale_selector=get_locale,
    timezone_selector=get_timezone,
    default_timezone="UTC",
    default_locale=app.config["LANGUAGES"][0],
)


@app.teardown_appcontext
def close_connection(s):
    storage.close()


@app.before_request
def auth_handler():
    """Auth handler function"""
    if auth is None:
        return
    if not auth.require_auth(
        request.path,
        [
            "/api/v1/status/",
            "/api/v1/auth/signup/",
            "/api/v1/auth/login/",
        ],
    ):
        return
    if (
        auth.authorization_header(request) is None
        and auth.session_cookie(request) is None
    ):
        abort(401)
    user = auth.current_user(request)
    if user is None:
        abort(403)
    request.current_user = user


@app.errorhandler(401)
def not_authorized(error) -> str:
    """Not authorized handler"""
    return jsonify({"error": _("unauthorized")}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """forbidden handler"""
    return jsonify({"error": _("forbidden")}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": _("not_found", data="user")}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
