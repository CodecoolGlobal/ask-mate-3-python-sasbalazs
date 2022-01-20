import psycopg2.sql

import connection
from datetime import datetime
import calendar


def add_new_tag_all(tag_name, question_id):
    add_new_tag(tag_name)
    tag_id_all = get_tag_id_from_name(tag_name)
    tag_id = tag_id_all[0]['id']
    add_tag_to_question(question_id, tag_id)


@connection.connection_handler
def delete_tag(cursor, question_id, tag_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            DELETE FROM question_tag
            WHERE question_id = {} AND tag_id={}
            """
        ).format(
        psycopg2.sql.Literal(question_id),
        psycopg2.sql.Literal(tag_id)
        )
    )


@connection.connection_handler
def add_tag_to_question(cursor, question_id, tag_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            INSERT INTO question_tag (question_id, tag_id)
            VALUES ({}, {})
            """ ).format(
            psycopg2.sql.Literal(question_id),
            psycopg2.sql.Literal(tag_id)
        )
    )


@connection.connection_handler
def add_new_tag(cursor, new_tag):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            INSERT INTO tag (name)
            VALUES ({})
            """ ).format(
            psycopg2.sql.Literal(new_tag)
        )
    )


def combine_tags_with_ids(question_id):
    tags = collect_all_tags(question_id)
    if tags:
        tag_ids = get_tag_id(question_id)
        tags_temp = [i[0]['name'] for i in tags]
        tag_ids_temp = [i['tag_id'] for i in tag_ids]
        tags_combined = list(zip(tags_temp, tag_ids_temp))
    else:
        tags_combined = None
    return tags_combined


def collect_all_tags(question_id):
    tag_id = get_tag_id(question_id)
    if tag_id:
        tag_ids = [i['tag_id'] for i in tag_id]
        tags = []
        for i in tag_ids:
            tag = get_tags(i)
            tags.append(tag)
        return tags
    else:
        return None


@connection.connection_handler
def get_tags(cursor, tag_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT name
            FROM tag
            WHERE id = {}"""
        ).format(
            psycopg2.sql.Literal(tag_id)
        )
    )
    return cursor.fetchall()

@connection.connection_handler
def get_tag_id_from_name(cursor, tag_name):
    cursor.execute(
        psycopg2.sql.SQL(
            '''
            SELECT id
            FROM tag
            WHERE name={}
            '''
        ).format(
            psycopg2.sql.Literal(tag_name)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def get_tag_id(cursor, question_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT tag_id
            FROM question_tag
            WHERE question_id = {}
            """
        ).format(
            psycopg2.sql.Literal(question_id)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def delete_question(cursor, question_id):
    query = """
            DELETE 
            FROM question
            WHERE id=%(question_id)s"""
    value = {'question_id': question_id}
    cursor.execute(query, value)


@connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
            DELETE 
            FROM answer
            WHERE id=%(answer_id)s
            """
    value = {'answer_id': answer_id}
    cursor.execute(query, value)


@connection.connection_handler
def get_question_id(cursor, answer_id):
    query = """
            SELECT question_id
            FROM answer
            WHERE "id"=%(answer_id)s"""
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
def q_title_search(cursor, search_phrase):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM question
            WHERE title LIKE {}"""
        ).format(
            psycopg2.sql.Literal('%' + search_phrase + '%')
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def q_message_search(cursor, search_phrase):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM question
            WHERE message LIKE {}"""
        ).format(
            psycopg2.sql.Literal('%' + search_phrase + '%')
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def a_search(cursor, search_phrase):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM answer
            WHERE message LIKE {}"""
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
def get_answer_to_edit(cursor, id):
    query = """
            SELECT *
            FROM answer
            WHERE id = %(id)s LIMIT 1"""
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchone()


@connection.connection_handler
def get_comment_to_edit(cursor, id):
    query = """
                SELECT *
                FROM comment
                WHERE id = %(id)s LIMIT 1"""
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchone()


@connection.connection_handler
def get_answers(cursor, question_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT *
            FROM answer
            WHERE question_id = {}
            ORDER BY submission_time"""
        ).format(psycopg2.sql.Literal(question_id))
    )
    return cursor.fetchall()


@connection.connection_handler
def get_comments(cursor, question_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """SELECT *
                FROM comment
                WHERE question_id = {}
                ORDER BY submission_time"""
        ).format(psycopg2.sql.Literal(question_id))
    )
    return cursor.fetchall()


@connection.connection_handler
def add_comments(cursor, data):
    query = """
            INSERT INTO comment 
            (question_id, message, submission_time, edited_count)
            VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_count)s)"""
    cursor.execute(query,
                   {"question_id": data[0], "message": data[1], "submission_time": data[2], "edited_count": data[3]})


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


@connection.connection_handler
def edit_question(cursor, title, message, image, id):
    cursor.execute("UPDATE question SET title = %s, message = %s, image = %s WHERE id = %s", (title, message, image, id))


@connection.connection_handler
def edit_answer(cursor, message, image, id):
    cursor.execute("UPDATE answer SET message = %s, image = %s WHERE id = %s", (message, image, id))


@connection.connection_handler
def edit_comment(cursor, message, submission_time, edited_count, id):
    cursor.execute("UPDATE comment SET message = %s, submission_time = %s, edited_count = %s WHERE id = %s",
                   (message, submission_time, edited_count, id))


def get_unixtime():
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    return unixtime


def convert_to_date(timestamp):
    ts = int(timestamp)
    data = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return data








