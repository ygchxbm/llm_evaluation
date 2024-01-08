from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func
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
    submit_user = db.Column(db.String(50))
    submit_time = db.Column(db.DateTime)
    submit_remark = db.Column(db.String(200))
    submit_timecost = db.Column(db.Integer)  # millisecond
    submit_count = db.Column(db.Integer)  # times of submit

    # 定义联合唯一索引
    __table_args__ = (
        db.UniqueConstraint('exam_id', 'question_id', 'submit_user_id'),
    )

    def __init__(self, exam_id=None, question_id=None, question=None, dimension=None, llm_answer=None, llm_timecost=None, llm_gen_count=None, submit_score=None, submit_user_id=None, submit_user=None, submit_time=None, submit_remark=None, submit_timecost=None, submit_count=None):
        self.exam_id = exam_id
        self.question_id = question_id
        self.question = question
        self.dimension = dimension
        self.llm_answer = llm_answer
        self.llm_timecost = llm_timecost
        self.llm_gen_count = llm_gen_count
        self.submit_score = submit_score
        self.submit_user_id = submit_user_id
        self.submit_user = submit_user
        self.submit_time = submit_time
        self.submit_remark = submit_remark
        self.submit_timecost = submit_timecost
        self.submit_count = submit_count

    @classmethod
    def get(cls, id):
        exam_detail = cls.query.filter(ExamDetail.id==id).first()
        return exam_detail

    @classmethod
    def get_answer(cls, exam_id, question_id, submit_user_id):
        llm_model = cls.query.filter(ExamDetail.exam_id==exam_id, ExamDetail.question_id==question_id, ExamDetail.submit_user_id==submit_user_id).first()
        return llm_model

    @classmethod
    def list(cls, exam_id):
        stu_obj = cls.query.filter(ExamDetail.exam_id == exam_id).all()
        return stu_obj

    @classmethod
    def list_4_other_answers(cls, exam_ids, question_ids):
        stu_obj = cls.query.filter(ExamDetail.exam_id.in_(exam_ids), ExamDetail.question_id.in_(question_ids), ExamDetail.submit_score >= 0).all()
        return stu_obj

    @classmethod
    def save_llm_answer(cls, id, exam_id, question_id, question, dimension, llm_answer, llm_timecost, llm_gen_count, submit_user_id, submit_user):
        # 假设my_table是你的数据表，data是你要插入或更新的数据
        insert_stmt = insert(ExamDetail).values(
            id=id,
            exam_id = exam_id,
            question_id = question_id,
            question = question,
            dimension = dimension,
            llm_answer = llm_answer,
            llm_timecost = llm_timecost,
            llm_gen_count = llm_gen_count,
            submit_user_id = submit_user_id,
            submit_user = submit_user,
        )

        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            llm_answer=llm_answer,
            llm_timecost=llm_timecost,
            llm_gen_count=llm_gen_count,
            updated_at=db.func.now(),
        )

        result = db.session.execute(on_duplicate_key_stmt)
        db.session.flush()
        db.session.commit()

        return result.lastrowid

    @classmethod
    def update_submit(cls, exam_detail_id, submit_score, submit_user_id, submit_user, submit_time, submit_remark, submit_timecost):

        # 修改数据
        cls.query.filter(ExamDetail.id == exam_detail_id).update({
            'submit_score': submit_score,
            'submit_user_id': submit_user_id,
            'submit_user': submit_user,
            'submit_time': submit_time,
            'submit_remark': submit_remark,
            'submit_timecost': submit_timecost,
            'submit_count': ExamDetail.submit_count + 1 if ExamDetail.submit_count is not None else 1,
            'updated_at': db.func.now(),
        })

        # 提交即保存到数据库
        db.session.commit()
        return True

    @classmethod
    def get_finished_submit_count(cls, exam_id, submit_user_id):
        count = cls.query.filter(ExamDetail.exam_id == exam_id, ExamDetail.submit_user_id == submit_user_id, ExamDetail.submit_score >= 0).count()
        return count

    @classmethod
    def get_submit_score(cls, exam_ids):
        result = db.session.query(func.sum(ExamDetail.submit_score), func.count(1), ExamDetail.dimension, ExamDetail.exam_id).filter(ExamDetail.submit_score >= 0, ExamDetail.exam_id.in_(exam_ids)).group_by(ExamDetail.exam_id, ExamDetail.dimension).all()

        return result

    @classmethod
    def get_submit_score_by_user_id(cls, exam_id):
        result = db.session.query(func.count(1), ExamDetail.submit_user_id).filter(ExamDetail.submit_score >= 0, ExamDetail.exam_id==exam_id).group_by(ExamDetail.submit_user_id).all()
        return result
