# Configurations like database URI, secret keys etc.


class Config:
    DEBUG = True
    SECRET_KEY = "quizquickie_secret_key"
    LANGUAGES = ["en", "fr", "ar"]
    SQLALCHEMY_DATABASE_URI = "sqlite:///quizquickie.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    SWAGGER = {"title": "QuizQuickie Restful API", "uiversion": 3}
