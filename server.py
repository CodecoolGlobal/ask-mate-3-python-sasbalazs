from flask import Flask, render_template, request, redirect, url_for, session, flash
import data_manager
import os

dirname = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(dirname, "static", "Image")
app = Flask(__name__)
app.config['LOGIN_STATE'] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_status = ''
    if request.method == 'POST':
        username = request.form['username']
        valid_username = data_manager.check_username(username)
        plain_text_password = request.form['password']
        valid_password = data_manager.check_password(valid_username['username'])
        is_matching = data_manager.verify_password(plain_text_password, valid_password['password'])
        if is_matching:
            session['username'] = username
            return redirect(url_for('main_page'))
        else:
            login_status = "Wrong password or username given!"
    return render_template('login.html', login_status=login_status)


@app.route("/list_users", methods=['GET', 'POST'])
def list_users():
    if "username" in session:
        users = data_manager.list_users()
        return render_template("users.html", users=users)
    else:
        return redirect("/")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main_page'))


@app.route("/register", methods=['GET', 'POST'])
def registration_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        time = data_manager.get_unixtime()
        submission_time = data_manager.convert_to_date(time)
        hashed_password = data_manager.hash_password(password)
        data_manager.register_user(email, hashed_password, submission_time)
        return redirect(url_for('main_page'))
    return render_template('registration.html')


@app.route("/answer/<answer_id>/commits")
def render_answer_with_commits(answer_id):
    answer = data_manager.get_answer(answer_id)
    comments_to_render = data_manager.get_comments_to_answer(answer_id)
    return render_template('answer_and_comments.html', answer=answer, comments_to_render=comments_to_render)


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect(url_for("question", question_id=question_id))


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def add_tag(question_id):
    if request.method == "GET":
        tags_combined = data_manager.combine_tags_with_ids(question_id)
        return render_template("add_tag.html", question_id=question_id, tags=tags_combined)
    elif request.method == "POST":
        if request.form["new_tag"]:
            tag_name = request.form.get('new_tag')
            data_manager.add_new_tag_all(tag_name, question_id)
        return redirect(url_for("question", question_id=question_id))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    if "username" in session:
        data_manager.delete_question(question_id)
        return redirect("/list")
    else:
        return redirect(url_for("question", question_id=int(question_id)))


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    if "username" in session:
        question_id = data_manager.get_question_id(answer_id)
        data_manager.delete_answer(answer_id)
        return redirect(url_for("question", question_id=question_id['question_id']))
    else:
        question_id = data_manager.get_question_id(answer_id)
        return redirect(url_for("question", question_id=question_id['question_id']))


@app.route("/comment/<comment_id>/delete")
def delete_comment(comment_id):
    if "username" in session:
        question_id = data_manager.get_question_id_from_comment_id(comment_id)
        data_manager.delete_comment(comment_id)
        return redirect(url_for("question", question_id=question_id['question_id']))
    else:
        question_id = data_manager.get_question_id_from_comment_id(comment_id)
        return redirect(url_for("question", question_id=question_id['question_id']))


@app.route("/answer-comment/<comment_id>/delete")
def delete_answer_comment(comment_id):
    answer_id = data_manager.get_answer_id_to_delete_comment(comment_id)
    answer_id = answer_id['answer_id']
    answer = data_manager.get_answer(answer_id)
    comments_to_render = data_manager.get_comments_to_answer(answer_id)
    if "username" in session:
        data_manager.delete_comment(comment_id)
        comments_to_render = data_manager.get_comments_to_answer(answer_id)
        return render_template('answer_and_comments.html', answer=answer, comments_to_render=comments_to_render)
    else:
        return render_template('answer_and_comments.html', answer=answer, comments_to_render=comments_to_render)


@app.route("/answer/<answer_id>/vote_up", methods=["GET"])
def vote_up_answer(answer_id):
    question_id = data_manager.get_question_id(answer_id)
    if request.method == 'GET':
        data_manager.a_vote_up(answer_id)
    return redirect(url_for("question", question_id=question_id['question_id']))


@app.route("/answer/<answer_id>/vote_down", methods=["GET"])
def vote_down_answer(answer_id):
    question_id = data_manager.get_question_id(answer_id)
    if request.method == "GET":
        data_manager.a_vote_down(answer_id)
    return redirect(url_for("question", question_id=question_id['question_id']))


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def post_new_answer(question_id):
    if "username" in session:
        username = session['username']
        if request.method == 'GET':
            route = url_for("post_new_answer", question_id=question_id)
            question_to_render = data_manager.get_last_question(question_id)
            return render_template('new_answer.html', route=route, question_id=question_id,
                                                     question_to_render=question_to_render)

        elif request.method == 'POST':
            if request.files['image']:
                file = request.files['image']
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            time = data_manager.get_unixtime()
            submission_time = data_manager.convert_to_date(time)
            vote_number = 0
            question_id = question_id
            message = request.form['new_answer']
            file = request.files['image']
            if file.filename:
                image = file.filename
            else:
                image = None
            accepted = False
            user_id = data_manager.get_user_id(username)
            data = [submission_time, vote_number, question_id, message, image, accepted, user_id['id']]
            data_manager.post_answer(data)
            return redirect(url_for("question", question_id=question_id))
    return redirect("/")



@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if "username" in session:
        username = session['username']
        if request.method == 'POST':
            if request.files['image']:
                file = request.files['image']
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            time = data_manager.get_unixtime()
            submission_time = data_manager.convert_to_date(time)
            view_number = 0
            vote_number = 0
            title = request.form['title']
            message = request.form['message']
            file = request.files['image']
            if file.filename:
                image = file.filename
            else:
                image = None
            user_id = data_manager.get_user_id(username)
            data = [submission_time, view_number,vote_number, title, message, image, user_id['id']]
            id = data_manager.addquestion(data)
            return redirect(url_for("display_question",id = id['id']))
        return render_template('add-question.html')
    return redirect("/")


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def render_comment_template(question_id):
    if "username" in session:
        return render_template('add_comment.html', question_id=question_id)
    else:
        return redirect(url_for("question", question_id=int(question_id)))


@app.route("/answer/<answer_id>/new-comment")
def render_comment_template_to_answer(answer_id):
    if "username" in session:
        question_id = data_manager.get_question_id(answer_id)
        question_id = question_id['question_id']
        return render_template('add_comment_to_answer.html', answer_id=answer_id, question_id=question_id)
    else:
        answer = data_manager.get_answer(answer_id)
        comments_to_render = data_manager.get_comments_to_answer(answer_id)
        return render_template('answer_and_comments.html', answer=answer, comments_to_render=comments_to_render)


@app.route("/add_comment", methods=['GET', 'POST'])
def add_comment():
    if "username" in session:
        username = session['username']
        if request.method == 'POST':
            question_id = request.form['question_id']
            message = request.form['message']
            time = data_manager.get_unixtime()
            submission_time = data_manager.convert_to_date(time)
            edited_count = 0
            user_id = data_manager.get_user_id(username)
            data = [question_id, message, submission_time, edited_count, user_id['id']]
            data_manager.add_comments(data)
            return redirect(url_for("question", question_id=question_id))
    else:
        return redirect("/")



@app.route("/add_comment_to_answer", methods=['GET', 'POST'])
def add_comment_to_answer():
    if "username" in session:
        username = session['username']
        if request.method == 'POST':
            question_id = request.form['question_id']
            answer_id = request.form['answer_id']
            message = request.form['message']
            time = data_manager.get_unixtime()
            submission_time = data_manager.convert_to_date(time)
            edited_count = 0
            user_id = data_manager.get_user_id(username)
            data = [answer_id, message, submission_time, edited_count, user_id['id']]
            data_manager.add_comment_answer(data)
            return redirect(url_for("question", question_id=question_id))
    return redirect("/")


@app.route("/question/<question_id>", methods=['GET', 'POST'])
def question(question_id):
    route = url_for("post_new_answer", question_id=question_id)
    question_to_render = data_manager.get_last_question(str(question_id))
    answers_to_render = data_manager.get_answers(question_id)
    tags_combined = data_manager.combine_tags_with_ids(question_id)
    comments_to_render = data_manager.get_comments(question_id)
    if 'username' in session:
        logged_in = True
    else:
        logged_in = False
    if request.method == 'POST':
        answer_id = request.form.get('answer_id')
        data_manager.accept_answer(answer_id)
    return render_template('question.html', question_to_render=question_to_render,
                           answers_to_render=answers_to_render, route=route, tags=tags_combined,
                           comments_to_render=comments_to_render, logged_in=logged_in)


@app.route("/question/<question_id>/edit")
def edit_question(question_id):
    if "username" in session:
        question_to_edit = data_manager.get_last_question(question_id)
        return render_template('display_question_to_edit.html', question_to_edit=question_to_edit)
    else:
        return redirect(url_for("question", question_id=int(question_id)))


@app.route("/answer/<answer_id>/edit")
def edit_answer(answer_id):
    if "username" in session:
        answer_to_edit = data_manager.get_answer_to_edit(answer_id)
        return render_template('display_answer_to_edit.html', answer_to_edit=answer_to_edit)
    else:
        question_id = data_manager.get_question_id(answer_id)
        return redirect(url_for("question", question_id=question_id['question_id']))


@app.route("/comment/<comment_id>/edit")
def edit_comment(comment_id):
    if "username" in session:
        comment_to_edit = data_manager.get_comment_to_edit(comment_id)
        return render_template('display_comment_to_edit.html', comment_to_edit=comment_to_edit)
    else:
        question_id = data_manager.get_question_id_from_comment_id(comment_id)
        return redirect(url_for("question", question_id=question_id['question_id']))


@app.route("/answer-comment/<comment_id>/edit")
def edit_answer_comment(comment_id):
    if "username" in session:
        comment_to_edit = data_manager.get_comment_to_edit(comment_id)
        return render_template('display_comment_to_edit_for_answer.html', comment_to_edit=comment_to_edit)
    else:
        answer_id = data_manager.get_answer_id_to_delete_comment(comment_id)
        answer_id = answer_id['answer_id']
        answer = data_manager.get_answer(answer_id)
        comments_to_render = data_manager.get_comments_to_answer(answer_id)
        return render_template('answer_and_comments.html', answer=answer, comments_to_render=comments_to_render)


@app.route('/display_question/<id>', methods=['GET', 'POST'])
def display_question(id):
    new_question = data_manager.display_question_after_adding(id)
    return render_template("display_added_question.html", new_question=new_question)


@app.route("/rewrite_one_question/<id>", methods=['GET', 'POST'])
def rewrite_one_question(id):
    if "username" in session:
        if request.method == 'POST':
            if request.files['image']:
                file = request.files['image']
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            title = request.form['title']
            message = request.form['message']
            file = request.files['image']
            if file.filename:
                image = file.filename
            else:
                image = None
            data_manager.edit_question(title, message, image, id)
            questions = data_manager.get_questions()
            return render_template('list.html', questions=questions)
    return redirect("/")


@app.route("/rewrite_one_answer/<answer_id>", methods=['GET', 'POST'])
def rewrite_one_answer(answer_id):
    if "username" in session:
        question_id = data_manager.get_question_id(answer_id)
        if request.method == 'POST':
            if request.files['image']:
                file = request.files['image']
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            message = request.form['message']
            file = request.files['image']
            if file.filename:
                image = file.filename
            else:
                image = None
            data_manager.edit_answer(message, image, answer_id)
            return redirect(url_for("question", question_id=question_id['question_id']))
    return redirect("/")


@app.route("/rewrite_one_comment/<comment_id>", methods=['GET', 'POST'])
def rewrite_one_comment(comment_id):
    if request.method == 'POST':
        message = request.form['message']
        time = data_manager.get_unixtime()
        submission_time = data_manager.convert_to_date(time)
        edited_count = int(request.form['edited_count'])
        edited_count += 1
        question_id = request.form['question_id']
        data_manager.edit_comment(message, submission_time, edited_count, comment_id)
        route = url_for("post_new_answer", question_id=question_id)
        question_to_render = data_manager.get_last_question(str(question_id))
        answers_to_render = data_manager.get_answers(question_id)
        comments_to_render = data_manager.get_comments(question_id)
        return render_template('question.html', question_to_render=question_to_render,
                               answers_to_render=answers_to_render, comments_to_render=comments_to_render,
                               route=route)


@app.route("/rewrite_answer_comment/<comment_id>", methods=['GET', 'POST'])
def rewrite_answer_comment(comment_id):
    if request.method == 'POST':
        message = request.form['message']
        time = data_manager.get_unixtime()
        submission_time = data_manager.convert_to_date(time)
        edited_count = int(request.form['edited_count'])
        edited_count += 1
        data_manager.edit_comment(message, submission_time, edited_count, comment_id)
        answer_id = data_manager.get_answer_id(comment_id)
        answer_id = answer_id['answer_id']
        answer = data_manager.get_answer(answer_id)
        comments_to_render = data_manager.get_comments_to_answer(answer_id)
        return render_template('answer_and_comments.html', answer=answer, comments_to_render=comments_to_render)


@app.route("/list", methods=["GET", "POST"])
def list_page():
    questions = data_manager.get_questions()
    if request.method == "GET":
        order_by = request.args.get('order_by')
        order_direction = request.args.get('order_direction')
        if order_by and order_direction:
            order_by = order_by.lower()
            order_by = order_by.replace(" ", "_")
            if order_direction == 'descending':
                order_direction = 'DESC'
            else:
                order_direction = 'ASC'
            questions = data_manager.get_sorted(order_by, order_direction)
    return render_template('list.html', questions=questions)


@app.route("/")
def main_page():
    questions = data_manager.get_five_latest_questions()
    return render_template('main-page.html', questions=questions)


@app.route("/question/<question_id>/vote_up", methods=['GET'])
def vote_up(question_id):
    if request.method == 'GET':
        data_manager.q_vote_up(question_id)
    return redirect('/list')


@app.route("/question/<question_id>/vote_down", methods=['GET'])
def vote_down(question_id):
    if request.method == 'GET':
        data_manager.q_vote_down(question_id)
    return redirect('/list')


@app.route("/search", methods=['GET'])
def search():
    if request.method == "GET":
        search_phrase = request.args.get("q")
        message_search_temp = data_manager.q_search(search_phrase)
        all_question_temp = data_manager.get_questions()
        all_answers_temp = data_manager.get_all_answers()
        answers_temp = data_manager.a_search(search_phrase)
        message_search = data_manager.fancy_search_result(search_phrase, message_search_temp)
        all_question = data_manager.fancy_search_result(search_phrase, all_question_temp)
        all_answers = data_manager.fancy_search_result(search_phrase, all_answers_temp)
        answers = data_manager.fancy_search_result(search_phrase, answers_temp)

    return render_template('search.html', question_to_render=message_search, answers_to_render=answers,
                           all_answers=all_answers, all_question=all_question)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
