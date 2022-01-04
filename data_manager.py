import connection
from datetime import datetime
import calendar


def get_id(filename):
    item_id = len(filename)
    return item_id


def get_unixtime():
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    return unixtime


def convert_to_date(timestamp):
    ts = int(timestamp)
    data = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return data


def sorting_by_time(data):
    pass


def get_answer_questions(question_id):
    questions = connection.import_data("sample_data/question.csv")
    answers = connection.import_data("sample_data/answer.csv")
    question_to_render = []
    answers_to_render = []
    for line in questions:
        if question_id == line['id']:
            question_to_render = line
    for answer in answers:
        if question_id == answer['question_id']:
            answers_to_render.append(answer)
    return question_to_render, answers_to_render
