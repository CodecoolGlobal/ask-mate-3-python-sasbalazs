import psycopg2.sql

import connection
from datetime import datetime
import calendar


@connection.connection_handler
def delete_question(cursor, question_id):
    query = """
            DELETE 
            FROM question
            WHERE 'id'=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
            DELETE 
            FROM answer
            WHERE 'id'=%(answer_id)s
            """
    cursor.execute(query, {'answer_id': answer_id})


@connection.connection_handler
def get_question_id(cursor, answer_id):
    query = """
            SELECT
            question_id
            FROM
            answer
            WHERE "id"=%(answer_id)s
            """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def get_questions(cursor):
    query = """
            SELECT *
            FROM question
            ORDER BY submission_time DESC"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_five_latest_questions(cursor):
    query = """
                SELECT *
                FROM question
                ORDER BY submission_time DESC LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def search(cursor, search_phrase):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM question, answer
            WHERE question.title LIKE {}"""
        ).format(
            psycopg2.sql.Literal('%' + search_phrase + '%')
        )
        or
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM question, answer
            WHERE question.message LIKE {}"""
        ).format(
            psycopg2.sql.Literal('%' + search_phrase + '%')
        )
        or
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM question, answer
            WHERE answer.message LIKE {}"""
        ).format(
            psycopg2.sql.Literal('%' + search_phrase + '%')
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def get_last_question(cursor, id):
    query = """
        SELECT *
        FROM question
        WHERE id = %(id)s LIMIT 1"""
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
def a_vote_up(cursor, answer_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            UPDATE answer
            SET vote_number = vote_number + 1
            WHERE id = {}"""
        ).format(psycopg2.sql.Literal(answer_id))
    )


@connection.connection_handler
def a_vote_down(cursor, answer_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            UPDATE answer
            SET vote_number = vote_number - 1
            WHERE id = {}"""
        ).format(psycopg2.sql.Literal(answer_id))
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

@connection.connection_handler
def post_answer(cursor, data):
    query = """
    INSERT INTO answer
    (submission_time, vote_number, question_id, message, image)
    VALUES (%(submission_time)s, %(vote_number)s, %(question)s, %(message)s, %(image)s)"""
    cursor.execute(query, {"submission_time": data[0], "vote_number": data[1], "question": data[2], "message": data[3],
                           "image": data[4]})

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







