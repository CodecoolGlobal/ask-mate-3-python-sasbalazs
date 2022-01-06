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
    answers = connection.import_data("sample_data/answer.csv")
    questions = connection.import_data("sample_data/question.csv")
    res_answers = [answer for answer in answers if answer["question_id"] != question_id]
    res_questions = [question for question in questions if question["id"] != question_id]
    connection.export_data(res_answers, 'sample_data/answer.csv')
    connection.export_data(res_questions, 'sample_data/question.csv')
    return redirect("/")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    answers_without_deleted = []
    answers = connection.import_data("sample_data/answer.csv")
    for answer in answers:
        if answer['id'] != answer_id:
            answers_without_deleted.append(answer)
        else:
            question_id = answer['question_id']
    connection.export_data(answers_without_deleted, "sample_data/answer.csv")
    route = url_for("post_new_answer", question_id=question_id)
    question_to_render, answers_to_render = data_manager.get_answer_questions(question_id)
    return render_template('question.html', question_to_render=question_to_render,
                           answers_to_render=answers_to_render, route=route)


@app.route("/answer/<answer_id>/vote_up")
def vote_up_answer(answer_id):
    answers = connection.import_data("sample_data/answer.csv")
    for answer in answers:
        if answer["id"] == answer_id:
            vote_up = int(answer["vote_number"])
            vote_up += 1
            answer["vote_number"] = vote_up
            question_id = answer["question_id"]
    connection.export_data(answers, 'sample_data/answer.csv')
    return redirect(url_for("question", question_id=question_id))


@app.route("/answer/<answer_id>/vote_down")
def vote_down_answer(answer_id):
    answers = connection.import_data("sample_data/answer.csv")
    for answer in answers:
        if answer["id"] == answer_id:
            vote_down = int(answer["vote_number"])
            vote_down -= 1
            answer["vote_number"] = vote_down
            question_id = answer["question_id"]
    connection.export_data(answers, 'sample_data/answer.csv')
    return redirect(url_for("question", question_id=question_id))


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
    counter = len(connection.import_data('sample_data/question.csv'))+1
    if request.method == 'POST':
        if request.files['file']:
            file = request.files['file']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        new_question = {}
        id = counter
        new_question['id'] = str(id)
        submission_time = data_manager.get_unixtime()
        new_question['submission_time'] = submission_time
        new_question['view_number'] = 0
        new_question['vote_number'] = 0
        title = request.form['title']
        new_question['title'] = title
        message = request.form['message']
        new_question['message'] = message
        file = request.files['file']
        if file.filename:
            new_question['image'] = file.filename
        else:
            new_question['image'] = None
        questions = connection.import_data('sample_data/question.csv')
        questions.append(new_question)
        connection.export_data(questions, 'sample_data/question.csv')
        return redirect(url_for("display_question"))
    return render_template('add-question.html')


@app.route("/question/<question_id>")
def question(question_id):
    route = url_for("post_new_answer", question_id=question_id)
    answers = connection.import_data("sample_data/answer.csv")
    questions = connection.import_data("sample_data/question.csv")
    question_to_render, answers_to_render = data_manager.get_answer_questions(question_id)
    return render_template('question.html', question_to_render=question_to_render,
                           answers_to_render=answers_to_render, route=route, questions=questions)


@app.route("/question/<question_id>/edit")
def edit_question(question_id):
    questions = connection.import_data("sample_data/question.csv")
    question_to_edit = {}
    for line in questions:
        if question_id == line['id']:
            question_to_edit = line
    return render_template('display_question_to_edit.html', question_to_edit=question_to_edit)


@app.route('/display_question', methods=['GET', 'POST'])
def display_question():
    questions = connection.import_data("sample_data/question.csv")
    new_question = questions[-1]
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
        else:
            edited_question.update({'image': image})

        questions = connection.import_data('sample_data/question.csv')
        for quest in questions:
            index = int(quest['id'])
            if quest['id'] == edited_question['id']:
                questions[index - 1] = edited_question
        connection.export_data(questions, 'sample_data/question.csv')
        questions = connection.import_data('sample_data/question.csv')
        return render_template('list.html', questions=questions)


@app.route("/list")
@app.route("/")
def list_page():
    questions = connection.import_data("sample_data/question.csv")
    answers = connection.import_data("sample_data/answer.csv")
    if request.method == 'GET':
        order_by = request.args.get('order_by')
        order_direction = request.args.get('order_direction')
        if order_by == 'Title' and order_direction == 'ascending':
            questions = sorted(questions, key=lambda questions: questions['title'].upper())
        if order_by == 'Title' and order_direction == 'descending':
            questions = sorted(questions, key=lambda questions: questions['title'].upper(), reverse=True)
        if order_by == 'Number of views' and order_direction == 'ascending':
            questions = sorted(questions, key=lambda questions: int(questions['view_number']))
        if order_by == 'Number of views' and order_direction == 'descending':
            questions = sorted(questions, key=lambda questions: int(questions['view_number']), reverse=True)
        if order_by == 'Submission time' and order_direction == 'ascending':
            questions = sorted(questions, key=lambda questions: int(questions['submission_time']))
        if order_by == 'Submission time' and order_direction == 'descending':
            questions = sorted(questions, key=lambda questions: int(questions['submission_time']), reverse=True)
        if order_by == 'Message' and order_direction == 'ascending':
            questions = sorted(questions, key=lambda questions: len(questions['message']))
        if order_by == 'Message' and order_direction == 'descending':
            questions = sorted(questions, key=lambda questions: len(questions['message']), reverse=True)
        if order_by == 'Number of votes' and order_direction == 'ascending':
            questions = sorted(questions, key=lambda questions: int(questions['vote_number']))
        if order_by == 'Number of votes' and order_direction == 'descending':
            questions = sorted(questions, key=lambda questions: int(questions['vote_number']), reverse=True)
    return render_template('list.html', questions=questions, answers=answers)


@app.route("/question/<question_id>/vote_up", methods=['GET'])
def vote_up(question_id):
    questions = connection.import_data("sample_data/question.csv")
    route = url_for("post_new_answer", question_id=question_id)
    if request.method == 'GET':
        index = int(question_id) - 1
        line = questions[index]
        change = int(line['vote_number']) + 1
        questions[index]['vote_number'] = str(change)
        connection.export_data(questions, 'sample_data/question.csv')
        return redirect('/list')
    return render_template('vote_up.html', route=route)


@app.route("/question/<question_id>/vote_down", methods=['GET'])
def vote_down(question_id):
    questions = connection.import_data("sample_data/question.csv")
    route = url_for("post_new_answer", question_id=question_id)
    if request.method == 'GET':
        index = int(question_id) - 1
        line = questions[index]
        change = int(line['vote_number']) - 1
        questions[index]['vote_number'] = str(change)
        connection.export_data(questions, 'sample_data/question.csv')
        return redirect('/list')
    return render_template('vote_down.html', route=route)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
