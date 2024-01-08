from . import db
from app.models import model
from enum import Enum

# https://dormousehole.readthedocs.io/en/latest/patterns/sqlalchemy.html
# 增删改查 https://blog.csdn.net/Co_zy/article/details/77937195


# 题目
class Question(model.BaseModel):
    __tablename__ = 'llme_question'

    question_set_id = db.Column(db.Integer, index=True, nullable=False)  # 题库id
    dimension = db.Column(db.String(50))
    question = db.Column(db.Text)  # 题目内容
    answer = db.Column(db.Text)

    def __init__(self, question_set_id=None, dimension=None, question=None, answer=None):
        self.question_set_id = question_set_id
        self.dimension = dimension
        self.question = question
        self.answer = answer

    @classmethod
    def get(cls, id):
        question = cls.query.filter(Question.id==id).first()
        return question

    @classmethod
    def list(cls, set_id):
        stu_obj = cls.query.filter(Question.question_set_id == set_id).all()
        return stu_obj

    @classmethod
    def adds(cls, question_set_id, questions_dict):
        questions = []
        for question_dict in questions_dict:
            questions.append(Question(question_set_id=question_set_id, dimension=question_dict['维度'], question=question_dict['问题'], answer=question_dict['参考答案']))
        db.session.add_all(questions)
        db.session.commit()
        return
