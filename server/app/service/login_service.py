import os
import time
import json
import requests
from urllib import parse
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.user import User


def login(code, redirect_uri):
    Log.info('llm_model_list')

    token = _get_token(code, redirect_uri)
    if token.get('error', None) is not None:
        return NotFoundError('登录失败')
    oasis_openid = token.get('openid', None)
    access_token = token.get('access_token', None)

    userinfo = User.get_by_openid(oasis_openid)
    if None == userinfo:
        userinfo = _get_userinfo(access_token, oasis_openid)
        if userinfo.get('error', None) is not None:
            return NotFoundError('登录失败')
        birthdate = userinfo.get('birthdate', None)
        email = userinfo.get('email', None)
        email_verified = userinfo.get('email_verified', None)
        family_name = userinfo.get('family_name', None)
        gender = userinfo.get('gender', None)
        given_name = userinfo.get('given_name', None)
        locale = userinfo.get('locale', None)
        middle_name = userinfo.get('middle_name', None)
        name = userinfo.get('name', None)
        phone_number = userinfo.get('phone_number', None)
        phone_number_verified = userinfo.get('phone_number_verified', None)
        picture = userinfo.get('picture', None)
        preferred_username = userinfo.get('preferred_username', None)
        profile = userinfo.get('profile', None)
        sub = userinfo.get('sub', None)
        oasis_updated_at = userinfo.get('oasis_updated_at', None)
        website = userinfo.get('website', None)
        zoneinfo = userinfo.get('zoneinfo', None)
        User.add(oasis_openid, birthdate, email, email_verified, family_name, gender,
                 given_name, locale, middle_name, name, phone_number, phone_number_verified,
                 picture, preferred_username, profile, sub, oasis_updated_at, website, zoneinfo)

        userinfo = User.get_by_openid(oasis_openid)
        if None == userinfo:
            return NotFoundError('登录失败')

    # 如果验证成功，创建 JWT token
    access_token = create_access_token(identity=userinfo.to_dict())

    return Success({
        'access_token': access_token,
        'expires_in': int(time.time())+int(os.environ.get('LLM_EVALUATION_JWT_ACCESS_TOKEN_EXPIRES'))-int(int(os.environ.get('LLM_EVALUATION_JWT_ACCESS_TOKEN_EXPIRES'))/5),
        'userinfo': userinfo.to_dict()
    })


def _get_token(code, redirect_uri):
    Log.info('_get_token')

    uri = "/oauth2/token"
    base_url = os.environ.get('LLM_EVALUATION_SERVER_OASIS_HOST')

    params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": os.environ.get('LLM_EVALUATION_SERVER_OASIS_CLIENT_ID'),
        "client_secret": os.environ.get('LLM_EVALUATION_SERVER_OASIS_CLIENT_SECRET'),
    }

    param_str = parse.urlencode(params)

    url = f'{base_url}{uri}'

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url=url, data=param_str, headers=headers)

    print(response.status_code)
    print(response.text)

    return response.json()

def _get_userinfo(access_token, openid):
    Log.info('_get_userinfo')

    uri = f"/userinfo?access_token={access_token}&openid={openid}"
    base_url = os.environ.get('LLM_EVALUATION_SERVER_OASIS_HOST')

    url = f'{base_url}{uri}'

    response = requests.get(url=url)

    print(response.status_code)
    print(response.text)

    return response.json()


