#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.routes import app_routes


@app_routes.route("/status", methods=["GET"], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
    Return:
      - on success: the status of the API
      - on error:
    """
    return jsonify({"status": "OK"})


@app_routes.route("/stats", strict_slashes=False)
def stats() -> str:
    """GET /api/v1/stats
    Return:
      - on success: the number of each objects
      - on error:
    """
    from models import classes, storage, User
    from flask import g
    from flask_babel import _

    user = getattr(g, "user", None)
    if user is None:
        return jsonify(_("unauthorized"))

    stats = {}
    for clsname, cls in classes.items():
        stats[clsname] = storage.query(cls).count()
    return jsonify(stats)
