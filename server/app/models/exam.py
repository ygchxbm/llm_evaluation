from sqlalchemy import create_engine, and_, or_
from . import db
from app.models import model

# https://dormousehole.readthedocs.io/en/latest/patterns/sqlalchemy.html
# 增删改查 https://blog.csdn.net/Co_zy/article/details/77937195


# 评测任务
class Exam(model.BaseModel):
    __tablename__ = 'llme_exam'

    create_user_id = db.Column(db.Integer, index=True, nullable=False)  # 创建人
    create_user = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime)  # 期限
    llm_model_id = db.Column(db.Integer, index=True, nullable=False)  # ai模型id
    question_set_id = db.Column(db.Integer, index=True, nullable=False)  # 题库id
    question_count = db.Column(db.Integer, default=0, nullable=False)  # 题目数量
    submit_count = db.Column(db.Integer, default=0, nullable=False)  # 提交数量
    submit_score = db.Column(db.Integer, nullable=False, default=-1)  # 提交分数

    def __init__(self, create_user_id=None, create_user=None, deadline=None, llm_model_id=None, question_set_id=None, question_count=None, submit_count=None, submit_score=None):
        self.create_user_id = create_user_id
        self.create_user = create_user
        self.deadline = deadline
        self.llm_model_id = llm_model_id
        self.question_set_id = question_set_id
        self.question_count = question_count
        self.submit_count = submit_count
        self.submit_score = submit_score

    @classmethod
    def get(cls, id):
        exam = cls.query.filter(Exam.id==id).first()
        return exam

    @classmethod
    def list_paginate(cls, page_num, page_size, llm_model_id, create_user_id, created_time_min, created_time_max):
        filters = [Exam.deleted_at.is_(None)]
        if create_user_id > 0:
            filters.append(Exam.create_user_id == create_user_id)
        if created_time_min:
            filters.append(Exam.created_at >= created_time_min)
        if created_time_max:
            filters.append(Exam.created_at <= created_time_max)
        if llm_model_id > 0:
            filters.append(Exam.llm_model_id == llm_model_id)
        stu_obj = cls.query.filter(and_(*filters)).paginate(page=page_num, per_page=page_size, error_out=False)
        return stu_obj

    @classmethod
    def list_4_model(cls, llm_model_id):
        stu_obj = cls.query.filter(Exam.llm_model_id==llm_model_id).all()
        return stu_obj

    @classmethod
    def list(cls, ids):
        if len(ids) > 0:
            stu_obj = cls.query.filter(Exam.id.in_(ids)).all()
        else:
            stu_obj = cls.query.all()
        return stu_obj

    @classmethod
    def add(cls, create_user_id, create_user, deadline, llm_model_id, question_set_id, question_count, submit_count):
        exam = Exam(create_user_id=create_user_id, create_user=create_user, deadline=deadline, llm_model_id=llm_model_id, question_set_id=question_set_id, question_count=question_count, submit_count=submit_count)
        db.session.add(exam)
        db.session.flush()
        db.session.commit()
        return exam

    @classmethod
    def update_submit_count(cls, exam_id, submit_count, submit_score):

        # 修改数据
        cls.query.filter(Exam.id == exam_id).update({
            'submit_count': submit_count,
            'submit_score': submit_score,
            'updated_at': db.func.now(),
        })

        # 提交即保存到数据库
        db.session.commit()
        return True
