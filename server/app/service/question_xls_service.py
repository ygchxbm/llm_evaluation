from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.question import Question
import xlrd


def import_question(set_id, file_data):
    Log.info('import_question')

    workbook = xlrd.open_workbook(file_contents=file_data.read())
    sheet = workbook.sheet_by_index(0)
    row_num = sheet.nrows
    titles = ['问题', '维度', '参考答案']
    questions = []
    for i in range(row_num):
        row_value = sheet.row_values(i)
        question_dict = dict(zip(titles, row_value))
        questions.append(question_dict)
    Question.adds(set_id, questions)

    return Success()


def export_question(set_id):
    Log.info('export_question')

    question_list = Question.list(set_id)
    questions = []
    for question in question_list:
        questions.append({'维度': question.dimension, '问题': question.question, '参考答案': question.answer})

    return Success({
        'question_list': questions,
    })
