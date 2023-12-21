from . import db
from app.models import model

# https://dormousehole.readthedocs.io/en/latest/patterns/sqlalchemy.html
# 增删改查 https://blog.csdn.net/Co_zy/article/details/77937195


# 评测任务
class Exam(model.BaseModel):
    __tablename__ = 'llme_exam'

    create_user_id = db.Column(db.Integer, index=True, nullable=False)  # 创建人
    create_user = ""
    deadline = db.Column(db.DateTime, nullable=False)  # 期限
    llm_model_id = db.Column(db.Integer, index=True, nullable=False)  # ai模型id
    question_set_id = db.Column(db.Integer, index=True, nullable=False)  # 题库id

    def __init__(self, ip=None, count=None):
        self.ip = ip
        self.count = count

    @classmethod
    def get_count(cls, ip):
        count = cls.query.filter(IpCount.ip==ip).first()
        if None == count:
            return 0            
        
        return count.count
    
    @classmethod
    def set_count(cls, ip, count):
        
        ipCount = cls.query.filter(IpCount.ip==ip).first()
        if None == ipCount:
            ipCount = IpCount(ip, count)
            db.session.add(ipCount)
            db.session.commit()
        
        ipCount.count = count
        db.session.commit()