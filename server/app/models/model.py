from datetime import datetime

from . import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 更新时间
    deleted_at = db.Column(db.DateTime)  # 删除时间

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}