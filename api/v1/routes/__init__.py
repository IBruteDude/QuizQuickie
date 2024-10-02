""" API Routes
"""

from flask import Blueprint

app_routes = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.routes.index import *
from api.v1.routes.auth import *
from api.v1.routes.user_profile import *
from api.v1.routes.user_groups import *
from api.v1.routes.user_quizzes import *
from api.v1.routes.profiles import *
from api.v1.routes.quizzes import *
from api.v1.routes.groups import *
from api.v1.routes.test_only_route import *
