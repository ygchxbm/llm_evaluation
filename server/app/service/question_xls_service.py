import os
import time
import calendar

from flask import send_file
from app.serializer.common import Success, ParamError
from app.log import Log
from ..models.question import Question
import pandas


def import_question(set_id, file_data):
    Log.info('import_question')

    file_name = file_data.filename
    suffix = os.path.splitext(file_name)[-1]
    if suffix != '.xls' and suffix != '.xlsx':
        return ParamError('文件格式错误')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    now_time = calendar.timegm(time.gmtime())
    upload_path = os.path.join(parent_dir, 'upload')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    upload_path = os.path.abspath(upload_path)
    file_path = upload_path+'/'+str(now_time)+'_'+file_name
    file_data.save(file_path)
    # url = os.getenv("LLM_EVALUATION_DOWNLOAD_PATH")+file_path

    old_questions = Question.list(set_id)

    questions = []
    df = pandas.read_excel(file_path, engine = 'openpyxl')
    for index, row in df.iterrows():
        参考答案 = row['参考答案']
        a = type(参考答案)
        if 参考答案 is None or type(参考答案) != str:
            参考答案 = ''
        is_old = False
        for old_question in old_questions:
            if old_question.dimension == row['维度'] and old_question.question == row['问题'] and old_question.answer == 参考答案 and old_question.question_set_id == set_id:
                is_old = True
                break
        if not is_old:
            questions.append({'维度': row['维度'], '问题': row['问题'], '参考答案': 参考答案})
    if len(questions) > 0:
        Question.adds(set_id, questions)

    os.remove(file_path)

    return Success("导入成功")


def export_question(set_id):
    Log.info('export_question')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    now_time = calendar.timegm(time.gmtime())
    download_path = os.path.join(parent_dir, 'download')
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    upload_path = os.path.abspath(download_path)
    file_path = upload_path + '/' + str(now_time) + '.xlsx'

    question_list = Question.list(set_id)
    questions = []
    for question in question_list:
        questions.append({'维度': question.dimension, '问题': question.question, '参考答案': question.answer})

    data = pandas.DataFrame(questions)
    data.to_excel(file_path)

    return send_file(file_path, as_attachment=True)
