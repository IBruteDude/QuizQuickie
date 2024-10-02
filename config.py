# Configurations like database URI, secret keys etc.


class Config:
    DEBUG = True
    SECRET_KEY = "quizquickie_secret_key"
    LANGUAGES = ["en", "fr", "ar"]
    UNPROTECTED_ROUTES = [
        "/apidocs/",
        "/apidocs/*",
        "/api/v1/test/<command>",
        "/api/v1/status/",
        "/api/v1/auth/signup/",
        "/api/v1/auth/login/",
        "/api/v1/profile",
        "/api/v1/profile/<int:user_id>",
        "/api/v1/profile/<int:user_id>/quiz",
        "/api/v1/quiz",
        "/api/v1/quiz/<int:quiz_id>",
        "/api/v1/quiz/<int:quiz_id>/stats",
        "/api/v1/group",
        "/api/v1/group/<int:group_id>/users",
        "/api/v1/group/<int:group_id>/quizzes",
    ]
    SQLALCHEMY_DATABASE_URI = "sqlite:///quizquickie.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    SWAGGER = {"title": "QuizQuickie Restful API", "uiversion": 3}
    CACHE_DEFAULT_TIMEOUT = 300


class DevelopmentConfig(Config):
    FLASK_ENV = "development"


class ProductionConfig(Config):
    DEBUG = False
    CACHE_TYPE = "SimpleCache"
    FLASK_ENV = "production"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
