import os
import time
from flask_jwt_extended import create_access_token
from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.user import User


def login(user_id):
    Log.info('llm_model_list')

    userinfo = User.get(user_id)
    if None == userinfo:
        return NotFoundError('user not found')

    # 如果验证成功，创建 JWT token
    access_token = create_access_token(identity=userinfo.name)

    return Success({
        'access_token': access_token,
        'expires_in': int(time.time())+int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES'))-int(int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES'))/5),
        'userinfo': userinfo.to_dict()
    })