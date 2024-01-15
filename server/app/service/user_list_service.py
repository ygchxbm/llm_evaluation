from flask import jsonify
from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.user import User


def user_list():
    Log.info('user_list')

    user_list = User.list([])
    for user in user_list:
        user.birthdate = None
        user.email = None
        user.email_verified = None
        user.family_name = None
        user.gender = None
        user.given_name = None
        user.locale = None
        user.middle_name = None
        user.phone_number = None
        user.phone_number_verified = None
        user.picture = None
        user.preferred_username = None
        user.profile = None
        user.sub = None
        user.oasis_updated_at = None
        user.website = None
        user.zoneinfo = None
        user.oasis_openid = None
    user_list = [user.to_dict() for user in user_list]

    return Success(user_list)