from . import db
from app.models import model
from enum import Enum

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
    scale = db.Column(db.Integer, nullable = False)  # 规模大小，单位：
    conclusion = db.Column(db.String(500))  # 结论
    conclusion_user_id = db.Column(db.Integer, index=True)  # 结论人
    conclusion_user = db.Column(db.String(50))

    def __init__(self, name=None, model_name=None, type_id=None, scale=None, conclusion=None, conclusion_user_id=None, conclusion_user=None):
        self.name = name
        self.model_name = model_name
        self.type_id = type_id
        self.scale = scale
        self.conclusion = conclusion
        self.conclusion_user_id = conclusion_user_id
        self.conclusion_user = conclusion_user

    @classmethod
    def list(cls):
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
        # 提交即保存到数据库
        db.session.commit()
        return True
