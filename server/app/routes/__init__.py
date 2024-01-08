from .exam import exam_bp
from .exam_detail import exam_detail_bp
from .question import question_bp
from .question_set import question_set_bp
from .llm_model import llm_model_bp
from .user import user_bp


def init_app(app):
    app.register_blueprint(exam_detail_bp, url_prefix="/api/exam_detail")
    app.register_blueprint(exam_bp, url_prefix="/api/exam")
    app.register_blueprint(question_bp, url_prefix="/api/question")
    app.register_blueprint(question_set_bp, url_prefix="/api/question_set")
    app.register_blueprint(llm_model_bp, url_prefix="/api/llm_model")
    app.register_blueprint(user_bp, url_prefix="/api/user")