from .question import question_bp
from .question_set import question_set_bp
from .llm_model import llm_model_bp
from .user import user_bp


def init_app(app):
    app.register_blueprint(question_bp, url_prefix="/question")
    app.register_blueprint(question_set_bp, url_prefix="/question_set")
    app.register_blueprint(llm_model_bp, url_prefix="/llm_model")
    app.register_blueprint(user_bp, url_prefix="/user")