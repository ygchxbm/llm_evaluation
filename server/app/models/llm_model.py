from . import db
from app.models import model
from enum import Enum
from sqlalchemy import UniqueConstraint

# https://dormousehole.readthedocs.io/en/latest/patterns/sqlalchemy.html
# 增删改查 https://blog.csdn.net/Co_zy/article/details/77937195


class LlmModelType(Enum):
    LLMMODELTypeYUXUNLIAN = 1  # 预训练
    LLMMODELTypeWEITIAO = 2  # 微调


# 题目
class LlmModel(model.BaseModel):
    __tablename__ = 'llme_llm_model'

    name = db.Column(db.String(50), index = True, unique = True, nullable = False)
    model_name = db.Column(db.String(50), index = True, nullable = False)
    type_id = db.Column(db.Integer, index = True, nullable = False)  # 模型类型，参考 LlmModelClass
    type = ""
    score = db.Column(db.Integer, nullable = False)
    score_detail = db.Column(db.Text)
    score_detail_question_set = db.Column(db.Text)
    question_set_exam_id = db.Column(db.Text)
    scale = db.Column(db.Integer, nullable = False)  # 规模大小，单位：
    conclusion = db.Column(db.String(500))  # 结论
    conclusion_user_id = db.Column(db.Integer, index=True)  # 结论人
    conclusion_user = db.Column(db.String(50))
    exam_count = db.Column(db.Integer)  # 考试次数

    # # 定义联合唯一索引
    # __table_args__ = (
    #     UniqueConstraint('name', 'deleted_at', name='uix_name'),
    #     UniqueConstraint('model_name', 'deleted_at', name='uix_model_name'),
    # )

    def __init__(self, name=None, model_name=None, type_id=None, scale=None, conclusion=None, conclusion_user_id=None, conclusion_user=None, exam_count=None):
        self.name = name
        self.model_name = model_name
        self.type_id = type_id
        self.scale = scale
        self.conclusion = conclusion
        self.conclusion_user_id = conclusion_user_id
        self.conclusion_user = conclusion_user
        self.exam_count = exam_count

    @classmethod
    def get(cls, id):
        llm_model = cls.query.filter(LlmModel.id==id).first()
        return llm_model

    @classmethod
    def list(cls, ids):
        if len(ids) > 0:
            stu_obj = cls.query.filter(LlmModel.id.in_(ids)).all()
        else:
            stu_obj = cls.query.all()
        for stu in stu_obj:
            stu.type = LlmModel(stu.type_id).name
        return stu_obj

    @classmethod
    def list_4_not_ids(cls, not_ids):
        if len(not_ids) > 0:
            stu_obj = cls.query.filter(~LlmModel.id.in_(not_ids)).all()
        else:
            stu_obj = cls.query.all()
        for stu in stu_obj:
            stu.type = LlmModel(stu.type_id).name
        return stu_obj
    
    @classmethod
    def modify(cls, id, name, conclusion, conclusion_user_id, conclusion_user):

        # 查询数据
        llm_model = cls.query.filter(LlmModel.id == id).one()
        if llm_model is None:
            return False

        # 修改数据
        llm_model.name = name
        llm_model.conclusion = conclusion
        llm_model.conclusion_user_id = conclusion_user_id
        llm_model.conclusion_user = conclusion_user
        llm_model.updated_at = db.func.now(),
        # 提交即保存到数据库
        db.session.commit()
        return True

    @classmethod
    def update_submit(cls, llm_model_id, exam_count, score, score_detail, score_detail_question_set, question_set_exam_id):
        update_dict = {
            'exam_count': exam_count,
            'score': score,
            'updated_at': db.func.now(),
        }
        if len(score_detail) > 0:
            update_dict['score_detail'] = score_detail
        if len(score_detail_question_set) > 0:
            update_dict['score_detail_question_set'] = score_detail_question_set
        if len(question_set_exam_id) > 0:
            update_dict['question_set_exam_id'] = question_set_exam_id

        # 修改数据
        cls.query.filter(LlmModel.id == llm_model_id).update(update_dict)

        # 提交即保存到数据库
        db.session.commit()
        return True
