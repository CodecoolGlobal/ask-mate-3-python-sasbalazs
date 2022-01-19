from flask import Flask, flash, render_template, request, redirect, url_for
import connection
import data_manager
import os

dirname = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(dirname, "static", "Image")
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


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
    if request.method == 'GET':
        data_manager.a_vote_up(answer_id)
    return redirect("/question/<question_id>")


@app.route("/answer/<answer_id>/vote_down", methods=["GET"])
def vote_down_answer(answer_id):
    if request.method == "GET":
        data_manager.a_vote_down(answer_id)
    return redirect("/question/<question_id>")


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def post_new_answer(question_id):
    if request.method == 'GET':
        route = url_for("post_new_answer", question_id=question_id)
        question_to_render, answers_to_render = data_manager.get_answer_questions(question_id)
        return render_template('new_answer.html', route=route, question_id=question_id,
                                                 question_to_render=question_to_render, )
    elif request.method == 'POST':
        if request.files['image']:
            file = request.files['image']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        answers = connection.import_data("sample_data/answer.csv")
        new_answer = {}
        last_element = answers[-1]
        id = int(last_element['id']) + 1
        new_answer['id'] = id
        new_answer['submission_time'] = data_manager.get_unixtime()
        new_answer['vote_number'] = 0
        new_answer['question_id'] = question_id
        new_answer['message'] = request.form['new_answer']
        file = request.files['image']
        if file.filename:
            new_answer['image'] = file.filename
        else:
            new_answer['image'] = None
        answers.append(new_answer)
        connection.export_data(answers, 'sample_data/answer.csv')
        return redirect(url_for("question", question_id=question_id))


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        if request.files['file']:
            file = request.files['file']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        time = data_manager.get_unixtime()
        submission_time = data_manager.convert_to_date(time)
        view_number = 0
        vote_number = 0
        title = request.form['title']
        message = request.form['message']
        file = request.files['file']
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
    return render_template('question.html', question_to_render=question_to_render,
                           answers_to_render=answers_to_render, route=route)


@app.route("/question/<question_id>/edit")
def edit_question(question_id):
    questions = connection.import_data("sample_data/question.csv")
    question_to_edit = {}
    for line in questions:
        if question_id == line['id']:
            question_to_edit = line
    return render_template('display_question_to_edit.html', question_to_edit=question_to_edit)


@app.route('/display_question/<id>', methods=['GET', 'POST'])
def display_question(id):
    new_question = data_manager.display_question_after_adding(id)
    return render_template("display_added_question.html", new_question=new_question)


@app.route("/rewrite_one_question", methods=['GET', 'POST'])
def rewrite_one_question():
    edited_question = {}
    if request.method == 'POST':
        if request.files['image']:
            file = request.files['image']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        id = request.form['id']
        edited_question.update({'id': id})

        submission_time = request.form['submission_time']
        edited_question.update({'submission_time': submission_time})

        view_number = request.form['view_number']
        edited_question.update({'view_number': view_number})

        vote_number = request.form['vote_number']
        edited_question.update({'vote_number': vote_number})

        title = request.form['title']
        edited_question.update({'title': title})

        message = request.form['message']
        edited_question.update({'message': message})

        file = request.files['image']
        if file.filename:
            edited_question.update({'image': file.filename})
        # else:
        #     edited_question.update({'image': image})

        questions = connection.import_data('sample_data/question.csv')
        questions = [edited_question if quest['id'] == edited_question['id'] else quest for quest in questions]
        connection.export_data(questions, 'sample_data/question.csv')
        questions = connection.import_data('sample_data/question.csv')
        return render_template('list.html', questions=questions)


@app.route("/list", methods=["GET", "POST"])
@app.route("/")
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


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
