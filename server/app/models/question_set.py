from datetime import datetime
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import UniqueConstraint

from . import db
from app.models import model
from .question import Question

# https://dormousehole.readthedocs.io/en/latest/patterns/sqlalchemy.html
# 增删改查 https://blog.csdn.net/Co_zy/article/details/77937195


# 题库
class QuestionSet(model.BaseModel):
    __tablename__ = 'llme_question_set'

    name = db.Column(db.String(50))  # 题库标题
    create_user_id = db.Column(db.Integer, index=True, nullable=False)  # 创建人
    create_user = db.Column(db.String(50))
    modify_user_id = db.Column(db.Integer, index=True, nullable=False)  # 最后修改人
    modify_user = db.Column(db.String(50))

    # # 定义联合唯一索引
    # __table_args__ = (
    #     UniqueConstraint('name', 'deleted_at', name='uix_name'),
    # )

    def __init__(self, name=None, create_user_id=None, create_user=None):
        self.name = name
        self.create_user_id = create_user_id
        self.create_user = create_user

    @classmethod
    def get(cls, id):
        question_set = cls.query.filter(QuestionSet.id==id, QuestionSet.deleted_at.is_(None)).first()
        return question_set

    @classmethod
    def list(cls, ids):
        if len(ids) > 0:
            stu_obj = cls.query.filter(QuestionSet.id.in_(ids), QuestionSet.deleted_at.is_(None)).all()
        else:
            stu_obj = cls.query.filter(QuestionSet.deleted_at.is_(None)).all()
        return stu_obj

    @classmethod
    def modify(cls, id, name, modify_user_id, modify_user):

        # 查询数据
        question_set = cls.query.filter(QuestionSet.id == id).first()
        if question_set is None:
            return question_set

        # 修改数据
        question_set.name = name
        question_set.modify_user_id = modify_user_id
        question_set.modify_user = modify_user
        # 提交即保存到数据库
        db.session.commit()
        return question_set

    @classmethod
    def delete(cls, id, modify_user_id, modify_user):

        try:
            # 查询数据
            question_set = cls.query.filter(QuestionSet.id == id).first()
            if question_set is None:
                return question_set

            # 修改数据
            question_set.deleted_at = datetime.now()
            question_set.modify_user_id = modify_user_id
            question_set.modify_user = modify_user

            questions = Question.query.filter(Question.question_set_id == id).all()
            for question in questions:
                question.deleted_at = datetime.now()
                question.modify_user_id = modify_user_id
                question.modify_user = modify_user

            # 提交即保存到数据库
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False


    @classmethod
    def save(cls, id, name, user_id, user):
        # 假设my_table是你的数据表，data是你要插入或更新的数据
        insert_stmt = insert(QuestionSet).values(
            id=id,
            name = name,
            create_user_id = user_id,
            create_user = user,
            modify_user_id = user_id,
            modify_user = user,
        )

        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            name = name,
            modify_user_id = user_id,
            modify_user = user,
            updated_at=db.func.now(),
        )

        result = db.session.execute(on_duplicate_key_stmt)
        db.session.flush()
        db.session.commit()

        return result.lastrowid
