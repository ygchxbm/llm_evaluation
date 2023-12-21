from . import db
from app.models import model

# https://dormousehole.readthedocs.io/en/latest/patterns/sqlalchemy.html
# 增删改查 https://blog.csdn.net/Co_zy/article/details/77937195


# 评测任务详情
class ExamDetail(model.BaseModel):
    __tablename__ = 'llme_exam_detail'

    exam_id = db.Column(db.Integer, index=True, nullable=False)  # 评测id
    question_id = db.Column(db.Integer, index=True, nullable=False)  # 问题id
    question = ""
    dimension = ""
    llm_answer = db.Column(db.Text)
    llm_timecost = db.Column(db.Integer)  # millisecond
    llm_gen_count = db.Column(db.Integer, nullable=False)
    submit_score = db.Column(db.Integer, nullable=False, default=-1)
    submit_user_id = db.Column(db.Integer, index=True, nullable=False)
    submit_user = ""
    submit_time = db.Column(db.DateTime, nullable=False)
    submit_remark = db.Column(db.String(200))
    submit_timecost = db.Column(db.Integer)  # millisecond
    submit_count = db.Column(db.Integer)  # times of submit

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