from . import db
from app.models import model

# https://dormousehole.readthedocs.io/en/latest/patterns/sqlalchemy.html
# 增删改查 https://blog.csdn.net/Co_zy/article/details/77937195


# 评测任务详情
class ExamDetail(model.BaseModel):
    __tablename__ = 'llme_exam_detail'

    exam_id = db.Column(db.Integer, index=True, nullable=False)  # 评测id
    question_id = db.Column(db.Integer, index=True, nullable=False)  # 问题id
    question = db.Column(db.Text)
    dimension = db.Column(db.String(50))
    llm_answer = db.Column(db.Text)
    llm_timecost = db.Column(db.Integer)  # millisecond
    llm_gen_count = db.Column(db.Integer, nullable=False)
    submit_score = db.Column(db.Integer, nullable=False, default=-1)
    submit_user_id = db.Column(db.Integer, index=True, nullable=False)
    submit_user = db.Column(db.String(50), nullable=False)
    submit_time = db.Column(db.DateTime, nullable=False)
    submit_remark = db.Column(db.String(200))
    submit_timecost = db.Column(db.Integer)  # millisecond
    submit_count = db.Column(db.Integer)  # times of submit

    def __init__(self, exam_id=None, question_id=None, llm_answer=None, llm_timecost=None, llm_gen_count=None, submit_score=None, submit_user_id=None, submit_time=None, submit_remark=None, submit_timecost=None, submit_count=None):
        self.exam_id = exam_id
        self.question_id = question_id
        self.llm_answer = llm_answer
        self.llm_timecost = llm_timecost
        self.llm_gen_count = llm_gen_count
        self.submit_score = submit_score
        self.submit_user_id = submit_user_id
        self.submit_time = submit_time
        self.submit_remark = submit_remark
        self.submit_timecost = submit_timecost
        self.submit_count = submit_count

    @classmethod
    def list(cls, exam_id):
        stu_obj = cls.query.filter(ExamDetail.exam_id == exam_id).all()
        return stu_obj

    @classmethod
    def list_4_other_answers(cls, exam_ids, question_ids):
        stu_obj = cls.query.filter(ExamDetail.exam_id.in_(exam_ids), ExamDetail.question_id.in_(question_ids), ExamDetail.submit_score >= 0).all()
        return stu_obj
