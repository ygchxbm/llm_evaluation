from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.user import User
from ..models.exam import Exam
from ..models.question_set import QuestionSet
from ..models.llm_model import LlmModel


def exam_list(page):
    Log.info('exam_list')

    exam_list = Exam.list_paginate(page)

    set_ids = [exam.question_set_id for exam in exam_list.items]
    question_set_list = QuestionSet.list(set_ids)

    # exam_list内的question_set_name替换为question_set_list中的name
    for exam in exam_list.items:
        for question_set in question_set_list:
            if exam.question_set_id == question_set.id:
                exam.question_set_name = question_set.name
                break
        else:
            return NotFoundError('question_set_id:{}'.format(exam.question_set_id))

    llm_model_ids = [exam.llm_model_id for exam in exam_list.items]
    llm_model_list = LlmModel.list(llm_model_ids)

    # exam_list内的llm_model_name替换为llm_model_list中的name
    for exam in exam_list.items:
        for llm_model in llm_model_list:
            if exam.llm_model_id == llm_model.id:
                exam.llm_model_name = llm_model.name
                break
        else:
            return NotFoundError('llm_model_id:{}'.format(exam.llm_model_id))

    return Success(exam_list.items)