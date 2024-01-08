from flask import Response, current_app
import typing as t
from werkzeug.exceptions import HTTPException

import json


class APIException(HTTPException):
    code = 200
    error_code = 3000
    message = '服务器内部错误'
    data = None

    def __init__(self, error_code=None, message=None, data=None) -> None:
        if error_code is not None:
            self.error_code = error_code
        if message is not None:
            self.message = message
        if data is not None:
            self.data = data
        super().__init__(message, None)

    def get_body(self, environ=None, scope=None) -> bytes:
        body = dict(
            code=self.error_code,
            message=self.message,
            data=self.data
        )
        return current_app.json.dumps(body)

    def get_headers(
        self, environ=None,
        scope=None,
    ):
        """Get a list of headers."""
        return [('Content-Type', 'application/json;charset=utf-8')]

    def to_dict(self):
        return dict(
            code=self.error_code,
            message=self.message,
            data=self.data
        )

    @classmethod
    def ok(cls, data=None):
        return cls(0, '', data)


def Success(data=None):
    return APIException.ok(data).to_dict()


class Base(APIException):
    error_code = 1000
    data = None
    message = '成功'

    def __init__(self, message=None):
        if message is not None:
            self.message = message
        super().__init__(self.error_code, self.message, self.data)


def List(total, items, page):
    return APIException.ok({
        'total': total,
        'items': items,
        'page': page
    }).to_dict()


class TokenError(Base):
    error_code = 2002
    data = None
    message = 'Token错误'


class TokenExpiredError(Base):
    error_code = 2003
    data = None
    message = 'Token过期'


class LoginError(Base):
    error_code = 2004
    data = None
    message = '用户名或密码错误'


class NotFoundError(Base):
    error_code = 2005
    data = None
    message = '资源未找到'


class ClientError(Base):
    error_code = 2006
    data = None
    message = '资源已存在'


class BasicAuthError(Base):
    error_code = 2007
    data = None
    message = 'Basic 鉴权失败'


class UnsupportedMethod(Base):
    error_code = 2008
    data = None
    message = '不支持的请求方法'


class ParamError(Base):
    error_code = 2009
    data = None
    message = '参数错误'


class ServerError(Base):
    error_code = 3000
    data = None
    message = '服务器内部错误'