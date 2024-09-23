from models.engine.relational_storage import RelationalStorage
from models.user import User
from models.group import Group
from models.group_user import group_user
from models.quiz import Quiz
from models.user_session import UserSession
from models.question import Question
from models.answer import Answer
from models.user_quiz_attempt import user_quiz_attempt
from models.quiz_attempt import QuizAttempt
from models.user_answer import UserAnswer

storage = RelationalStorage()
storage.reload()
