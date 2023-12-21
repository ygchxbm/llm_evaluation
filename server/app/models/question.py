from . import db
from app.models import model
from enum import Enum

# https://dormousehole.readthedocs.io/en/latest/patterns/sqlalchemy.html
# 增删改查 https://blog.csdn.net/Co_zy/article/details/77937195


class QuestionDimension(Enum):
    QUESTDIMENSIONJSBY = 1  # 角色扮演


# 题目
class Question(model.BaseModel):
    __tablename__ = 'llme_question'

    question_set_id = db.Column(db.Integer, index=True, nullable=False)  # 题库id
    dimension_id = db.Column(db.Integer, index=True, nullable=False)  # 题目类型id，参考枚举 QuestionDimension
    dimension = ""
    question = db.Column(db.Text)  # 题目内容
    answer = db.Column(db.Text)

    def __init__(self, question_bank_id=None, dimension_id=None, question=None, answer=None):
        self.question_bank_id = question_bank_id
        self.dimension_id = dimension_id
        self.question = question
        self.answer = answer

    @classmethod
    def list(cls, set_id):
        stu_obj = cls.query.filter(Question.question_set_id == set_id).all()
        return stu_obj