from flask import Flask, flash, render_template, request, redirect, url_for
import connection
import data_manager
import os

dirname = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(dirname, "static", "Image")
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect(url_for("question", question_id=question_id))


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def add_tag(question_id):
    if request.method == "GET":
        return render_template("add_tag.html", question_id=question_id)
    elif request.method == "POST":
        if request.form['tag_id']:
            tag_id = request.form.get('tag_id')
            print(tag_id, question_id)
            data_manager.add_tag_to_question(question_id, tag_id)
        elif request.form["new_tag"]:
            tag_name = request.form.get('new_tag')
            data_manager.add_new_tag(tag_name)
        return redirect(url_for("question", question_id=question_id['question_id']))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect("/")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    question_id = data_manager.get_question_id(answer_id)
    data_manager.delete_answer(answer_id)
    return redirect(url_for("question", question_id=question_id['question_id']))


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
    if request.method == 'GET':
        route = url_for("post_new_answer", question_id=question_id)
        question_to_render = data_manager.get_last_question(question_id)
        answers_to_render = data_manager.get_answers(question_id)
        return render_template('new_answer.html', route=route, question_id=question_id,
                                                 question_to_render=question_to_render, )
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
        data = [submission_time, vote_number, question_id, message, image]
        data_manager.post_answer(data)
        return redirect(url_for("question", question_id=question_id))


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
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
        data = [submission_time, view_number,vote_number, title, message, image]
        id = data_manager.addquestion(data)
        return redirect(url_for("display_question",id = id['id']))
    return render_template('add-question.html')


@app.route("/question/<question_id>")
def question(question_id):
    route = url_for("post_new_answer", question_id=question_id)
    question_to_render = data_manager.get_last_question(str(question_id))
    answers_to_render = data_manager.get_answers(question_id)
    tags_combined = data_manager.combine_tags_with_ids(question_id)
    return render_template('question.html', question_to_render=question_to_render,
                           answers_to_render=answers_to_render, route=route, tags=tags_combined)


@app.route("/question/<question_id>/edit")
def edit_question(question_id):
    question_to_edit = data_manager.get_last_question(question_id)
    return render_template('display_question_to_edit.html', question_to_edit=question_to_edit)


@app.route('/display_question/<id>', methods=['GET', 'POST'])
def display_question(id):
    new_question = data_manager.display_question_after_adding(id)
    return render_template("display_added_question.html", new_question=new_question)


@app.route("/rewrite_one_question/<id>", methods=['GET', 'POST'])
def rewrite_one_question(id):
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
    return redirect('/list')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
