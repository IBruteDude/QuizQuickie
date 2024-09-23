#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_routes = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.routes.index import *
from models import storage

storage.reload()
