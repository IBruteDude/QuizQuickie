#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.routes import app_routes


@app_routes.route("/status", methods=["GET"], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_routes.route("/stats", strict_slashes=False)
def stats() -> str:
    """GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from project_setup_script.models.engine.relational_storage import classes

    stats = {}
    for clsname, cls in classes.items():
        stats[clsname] = cls.count()
    return jsonify(stats)
