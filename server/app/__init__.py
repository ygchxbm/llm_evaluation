from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from . import routes, models
from .config import config
from .log import Log

# flask run命令会自动调用create_app函数 https://dormousehole.readthedocs.io/en/latest/cli.html
# 通过flask run启动时，可以通过设置FLASK_APP=app:create_app('development')来指定create_app的参数
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    Log.init_app('INFO')

    jwt = JWTManager(app)
    models.init_app(app)
    routes.init_app(app)

    Log.info('create_app:({})'.format(config_name))

    return app
