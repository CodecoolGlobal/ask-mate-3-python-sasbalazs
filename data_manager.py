import psycopg2.sql
import bcrypt

import connection
from datetime import datetime
import calendar


@connection.connection_handler
def get_user_data_from_id(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT id, username, registration_time, questions, answers, comments, reputation
            FROM users
            WHERE id={}
            """
        ).format(
            psycopg2.sql.Literal(user_id),
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def get_questions_by_user(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT id, title
            FROM question
            WHERE user_id = {} 
            """
        ).format(
            psycopg2.sql.Literal(user_id)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def get_answers_by_user(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT answer.message, question.title, question.id
            FROM answer
            JOIN question
            ON question.id=answer.question_id
            WHERE answer.user_id={}
            GROUP BY answer.message, question.title, question.id
            """
        ).format(
            psycopg2.sql.Literal(user_id)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def get_comments_by_user(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT comment.answer_id, comment.question_id, comment.message AS comment_message,
                   q1.title AS title, q1.id AS question_id, answer.message AS answer_message,
                   q2.id AS id, q2.title AS q2_title
            FROM comment
            LEFT JOIN question Q1
            ON q1.id=comment.question_id
            LEFT JOIN answer
            ON comment.answer_id=answer.id
            LEFT JOIN question q2
            ON answer.question_id=q2.id
            WHERE comment.user_id={}
            """
        ).format(
            psycopg2.sql.Literal(user_id)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def count_of_user_questions(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT COUNT(*)
            FROM question
            WHERE user_id = {} 
            """
        ).format(
            psycopg2.sql.Literal(user_id)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def get_user_name_from_name(cursor, username):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT id
            FROM users
            WHERE username={}
            """
        ).format(
        psycopg2.sql.Literal(username),
        )
    )
    return cursor.fetchone()


@connection.connection_handler
def update_question_column_of_user(cursor, user, sum_question):
    cursor.execute("UPDATE users SET questions = %s WHERE id = %s", (sum_question, user))


@connection.connection_handler
def count_of_user_answers(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT COUNT(*)
            FROM answer
            WHERE user_id = {} 
            """
        ).format(
            psycopg2.sql.Literal(user_id)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def update_answer_column_of_user(cursor, user, sum_answers):
    cursor.execute("UPDATE users SET answers = %s WHERE id = %s", (sum_answers, user))


@connection.connection_handler
def count_of_user_comments(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT COUNT(*)
            FROM comment
            WHERE user_id = {} 
            """
        ).format(
            psycopg2.sql.Literal(user_id)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def get_all_tags_and_usage(cursor):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT tag.id, tag.name, question.title, question.id AS question_id
            FROM tag
            JOIN question_tag
            ON tag.id=question_tag.tag_id
            JOIN question
            ON question.id=question_tag.question_id
            GROUP BY tag.id, question.title, question.id
            ORDER BY tag.id
            """
        ).format(
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def update_comment_column_of_user(cursor, user, sum_comments):
    cursor.execute("UPDATE users SET comments = %s WHERE id = %s", (sum_comments, user))


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


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def list_users(cursor):
    cursor.execute("""SELECT * FROM users""")
    return cursor.fetchall()


@connection.connection_handler
def get_user_id(cursor, username):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT id
            FROM users
            WHERE username = {}
            """).format(
            psycopg2.sql.Literal(username)
        )
    )
    return cursor.fetchone()


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
def check_username(cursor, username):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT username
            FROM users
            WHERE username = {}
            """).format(
            psycopg2.sql.Literal(username)
        )
    )
    return cursor.fetchone()


@connection.connection_handler
def get_password(cursor, username):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT password
            FROM users
            WHERE username = {}
            """).format(
            psycopg2.sql.Literal(username)
        )
    )
    return cursor.fetchone()


@connection.connection_handler
def register_user(cursor, email, password, r_time):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            INSERT INTO users
            (username, password, registration_time)
            VALUES ({}, {}, {})
            """).format(
            psycopg2.sql.Literal(email),
            psycopg2.sql.Literal(password),
            psycopg2.sql.Literal(r_time)
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
def delete_comment(cursor, comment_id):
    query = """
            DELETE 
            FROM comment
            WHERE id = %(comment_id)s
            """
    value = {'comment_id': comment_id}
    cursor.execute(query, value)


@connection.connection_handler
def get_question_id(cursor, answer_id):
    query = """
            SELECT question_id
            FROM answer
            WHERE answer.id = %(id)s"""
    cursor.execute(query, {'id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def get_answer(cursor, answer_id):
    query = """
            SELECT *
            FROM answer
            WHERE answer.id = %(id)s"""
    cursor.execute(query, {'id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def get_answer_id(cursor, comment_id):
    query = """
                SELECT answer_id
                FROM comment
                WHERE comment.id = %(id)s"""
    cursor.execute(query, {'id': comment_id})
    return cursor.fetchone()


@connection.connection_handler
def get_question_id_from_comment_id(cursor, comment_id):
    query = """
            SELECT question_id
            FROM comment
            WHERE comment.id = %(id)s"""
    cursor.execute(query, {'id': comment_id})
    return cursor.fetchone()


@connection.connection_handler
def get_answer_id_to_delete_comment(cursor, comment_id):
    query = """
            SELECT answer_id
            FROM comment
            WHERE comment.id = %(id)s"""
    cursor.execute(query, {'id': comment_id})
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
def q_search(cursor, search_phrase):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM question
            WHERE message LIKE {}
            OR title LIKE {}"""
        ).format(
            psycopg2.sql.Literal('%' + search_phrase + '%'),
            psycopg2.sql.Literal('%' + search_phrase + '%')
        )
    )
    return cursor.fetchall()


def fancy_search_result(search_phrase, text):
    new_value = f'<span style = "color: #ff0000"> {search_phrase} </span>'
    for i in text:
        # text[0]['title'] = i['title'].replace(search_phrase, new_value)
        text[0]['message'] = i['message'].replace(search_phrase, new_value)
    return text


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
def get_last_question(cursor, question_id):
    query = """
        SELECT *
        FROM question
        WHERE question.id = %(id)s LIMIT 1"""
    value = {'id': question_id}
    cursor.execute(query, value)
    return cursor.fetchone()


@connection.connection_handler
def get_answer_to_edit(cursor, answer_id):
    query = """
            SELECT *
            FROM answer
            WHERE answer.id = %(id)s LIMIT 1"""
    value = {'id': answer_id}
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
def get_all_answers(cursor):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT *
            FROM answer
            ORDER BY submission_time"""
        )
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
def get_comments_to_answer(cursor, answer_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """SELECT *
                FROM comment
                WHERE answer_id = {}
                ORDER BY submission_time"""
        ).format(psycopg2.sql.Literal(answer_id))
    )
    return cursor.fetchall()


@connection.connection_handler
def add_comments(cursor, data):
    query = """
            INSERT INTO comment 
            (question_id, message, submission_time, edited_count, user_id)
            VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_count)s, %(user_id)s)"""
    cursor.execute(query,
                   {"question_id": data[0], "message": data[1], "submission_time": data[2], "edited_count": data[3], "user_id": data[4]})


@connection.connection_handler
def add_comment_answer(cursor, data):
    query = """
                INSERT INTO comment 
                (answer_id, message, submission_time, edited_count, user_id)
                VALUES (%(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s, %(user_id)s)"""
    cursor.execute(query,
                   {"answer_id": data[0], "message": data[1], "submission_time": data[2], "edited_count": data[3], "user_id": data[4]})


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
    (submission_time, view_number, vote_number, title, message, image, user_id)
    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s, %(user_id)s)
    RETURNING id"""
    cursor.execute(query, {"submission_time": data[0], "view_number": data[1], "vote_number": data[2], "title": data[3],
                           "message": data[4], "image": data[5], "user_id": data[6]})
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
    (submission_time, vote_number, question_id, message, image, accepted, user_id)
    VALUES (%(submission_time)s, %(vote_number)s, %(question)s, %(message)s, %(image)s, %(accepted)s, %(user_id)s)"""
    cursor.execute(query, {"submission_time": data[0], "vote_number": data[1], "question": data[2], "message": data[3],
                           "image": data[4], "accepted": data[5], "user_id": data[6]})


@connection.connection_handler
def accept_answer(cursor, answer_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            UPDATE answer
            SET accepted = NOT accepted
            WHERE id = {}"""
        ).format(psycopg2.sql.Literal(answer_id))
    )


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


@connection.connection_handler
def get_bonus_questions(cursor):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT *
            FROM bonus_question"""
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def bonus_q_search(cursor, search_phrase):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM bonus_question
            WHERE message LIKE {}
            OR title LIKE {}"""
        ).format(
            psycopg2.sql.Literal('%' + search_phrase + '%'),
            psycopg2.sql.Literal('%' + search_phrase + '%')
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def not_bonus_q_search(cursor, title, message):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM bonus_question
            WHERE message != {}
            OR title != {}"""
        ).format(
            psycopg2.sql.Literal(message),
            psycopg2.sql.Literal(title)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def bonus_extra_q_search(cursor, filter_by, column):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM bonus_question
            WHERE {} LIKE {}"""
        ).format(
            psycopg2.sql.Identifier(column),
            psycopg2.sql.Literal('%' + filter_by + '%')
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def not_bonus_extra_q_search(cursor, filter_by, column):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM bonus_question
            WHERE {} != {}"""
        ).format(
            psycopg2.sql.Identifier(column),
            psycopg2.sql.Literal(filter_by)
        )
    )
    return cursor.fetchall()


@connection.connection_handler
def get_bonus_sorted(cursor, order_by, order_direction):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            SELECT * 
            FROM bonus_question
            ORDER BY {} {}"""
        ).format(
            psycopg2.sql.Identifier(order_by),
            psycopg2.sql.SQL(order_direction)
        )
    )
    return cursor.fetchall()


counter = 0


def get_unixtime():
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    return unixtime


def convert_to_date(timestamp):
    ts = int(timestamp)
    data = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return data


@connection.connection_handler
def get_userid_from_question(cursor, question_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """SELECT user_id
                FROM question
                WHERE question.id = {}"""
        ).format(psycopg2.sql.Literal(question_id)))
    return cursor.fetchone()


@connection.connection_handler
def update_reputation_up_by_question(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            UPDATE users
            SET reputation = reputation + 5
            WHERE id = {}"""
        ).format(psycopg2.sql.Literal(user_id))
    )

@connection.connection_handler
def update_reputation_down_by_question(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            UPDATE users
            SET reputation = reputation - 2
            WHERE id = {}"""
        ).format(psycopg2.sql.Literal(user_id))
    )


@connection.connection_handler
def get_userid_from_answer(cursor, answer_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """SELECT user_id
                FROM answer
                WHERE answer.id = {}"""
        ).format(psycopg2.sql.Literal(answer_id)))
    return cursor.fetchone()


@connection.connection_handler
def update_reputation_up_by_answer(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            UPDATE users
            SET reputation = reputation + 10
            WHERE id = {}"""
        ).format(psycopg2.sql.Literal(user_id))
    )

@connection.connection_handler
def update_reputation_down_by_answer(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            UPDATE users
            SET reputation = reputation - 2
            WHERE id = {}"""
        ).format(psycopg2.sql.Literal(user_id))
    )

@connection.connection_handler
def update_reputation_by_accepted_answer(cursor, user_id):
    cursor.execute(
        psycopg2.sql.SQL(
            """
            UPDATE users
            SET reputation = reputation + 15
            WHERE id = {}"""
        ).format(psycopg2.sql.Literal(user_id))
    )

@connection.connection_handler
def ask_accept_status_of_answer(cursor, answer_id):
    query = """
            SELECT accepted
            FROM answer
            WHERE id = %(id)s"""
    value = {'id': answer_id}
    cursor.execute(query, value)
    return cursor.fetchone()