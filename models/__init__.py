from models.engine.relational_storage import RelationalStorage
from models.user import User
from models.group import Group
from models.group_user import group_user
from models.quiz import Quiz
from models.user_session import UserSession
from models.question import Question
from models.answer import Answer
from models.quiz_attempt import QuizAttempt
from models.user_answer import UserAnswer
from models.ownership import Ownership
from bcrypt import hashpw, gensalt

classes = {
    "user": User,
    "group": Group,
    "quiz": Quiz,
    "user_session": UserSession,
    "question": Question,
    "answer": Answer,
    "quiz_attempt": QuizAttempt,
    "user_answer": UserAnswer,
    "ownership": Ownership,
}

storage = RelationalStorage()
storage.reload()

# if storage.query(User).where(User.user_name == 'admin').one_or_none() is None:
# 	admin = storage.new(User(email='admin@quizquickie.com', password=hashpw('admin'.encode(), gensalt()), user_name='admin')).save()
