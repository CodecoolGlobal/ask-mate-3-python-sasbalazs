import psycopg2.sql

import connection
from datetime import datetime
import calendar


@connection.connection_handler
def get_questions(cursor):
    query = """
            SELECT *
            FROM question
            ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_last_question(cursor, id):
    query = """
        SELECT *
        FROM question
        WHERE id = %(id)s LIMIT 1;"""
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchone()


@connection.connection_handler
def get_answers(cursor, question_id):
    query = """
                SELECT *
                FROM answer
                WHERE question_id = question_id
                ORDER BY submission_time"""
    value = {'question_id': question_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_sorted(cursor, order_by, order_direction):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM question
            ORDER BY {} {}"""
        ).format(
            psycopg2.sql.Identifier(order_by),
            psycopg2.sql.SQL(order_direction)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def q_vote_up(cursor, question_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            UPDATE question
            SET vote_number = vote_number + 1
            WHERE id = {}"""
        ).format(psycopg2.sql.Literal(question_id))
    )


@connection.connection_handler
def q_vote_down(cursor, question_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            UPDATE question
            SET vote_number = vote_number - 1
            WHERE id = {}"""
        ).format(psycopg2.sql.Literal(question_id))
    )


@connection.connection_handler
def addquestion(cursor, data):
    query = """
    INSERT INTO question 
    (submission_time, view_number, vote_number, title, message, image)
    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)
    RETURNING id"""
    cursor.execute(query, {"submission_time": data[0], "view_number": data[1], "vote_number": data[2], "title": data[3], "message": data[4], "image": data[5]})
    return cursor.fetchone()


@connection.connection_handler
def display_question_after_adding(cursor, id):
    query = """
            SELECT *
            FROM question
            WHERE id = %(id)s"""
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchone()


def get_unixtime():
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    return unixtime


def convert_to_date(timestamp):
    ts = int(timestamp)
    data = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return data


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


def delete_question(question_id):
    answers = connection.import_data("sample_data/answer.csv")
    questions = connection.import_data("sample_data/question.csv")
    res_answers = [answer for answer in answers if answer["question_id"] != question_id]
    res_questions = [question for question in questions if question["id"] != question_id]
    connection.export_data(res_answers, 'sample_data/answer.csv')
    connection.export_data(res_questions, 'sample_data/question.csv')





