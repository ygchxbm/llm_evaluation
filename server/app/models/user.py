from . import db
from app.models import model

# https://dormousehole.readthedocs.io/en/latest/patterns/sqlalchemy.html
# 增删改查 https://blog.csdn.net/Co_zy/article/details/77937195


# 用户
class User(model.BaseModel):
    __tablename__ = 'llme_user'

    oasis_openid = db.Column(db.String(255), index = True, unique = True, nullable=False)  # oasis平台openid
    birthdate = db.Column(db.String(255))
    email = db.Column(db.String(255))
    email_verified = db.Column(db.Boolean)
    family_name = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    given_name = db.Column(db.String(255))
    locale = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    phone_number_verified = db.Column(db.Boolean)
    picture = db.Column(db.String(255))
    preferred_username = db.Column(db.String(255))
    profile = db.Column(db.String(255))
    sub = db.Column(db.String(255))
    oasis_updated_at = db.Column(db.Integer)
    website = db.Column(db.String(255))
    zoneinfo = db.Column(db.String(255))

    def __init__(self, oasis_openid=None, birthdate=None, email=None, email_verified=None, family_name=None, gender=None,
                 given_name=None, locale=None, middle_name=None, name=None, phone_number=None, phone_number_verified=None,
                 picture=None, preferred_username=None, profile=None, sub=None, oasis_updated_at=None, website=None, zoneinfo=None):
        self.oasis_openid = oasis_openid
        self.birthdate = birthdate
        self.email = email
        self.email_verified = email_verified
        self.family_name = family_name
        self.gender = gender
        self.given_name = given_name
        self.locale = locale
        self.middle_name = middle_name
        self.name = name
        self.phone_number = phone_number
        self.phone_number_verified = phone_number_verified
        self.picture = picture
        self.preferred_username = preferred_username
        self.profile = profile
        self.sub = sub
        self.oasis_updated_at = oasis_updated_at
        self.website = website
        self.zoneinfo = zoneinfo

    @classmethod
    def get(cls, user_id):
        user = cls.query.filter(User.id==user_id).first()
        return user

    @classmethod
    def list(cls, ids):
        if len(ids) > 0:
            stu_obj = cls.query.filter(User.id.in_(ids)).all()
        else:
            stu_obj = cls.query.all()
        return stu_obj