from flask import Flask, flash, render_template, request, redirect, url_for
import connection
import data_manager

app = Flask(__name__)


@app.route("/question/<question_id>/new-answer", methods= ['GET', 'POST'])
def post_new_answer(question_id):
    if request.method == 'GET':
        route = url_for("post_new_answer", question_id=question_id)
        question_to_render, answers_to_render = data_manager.get_answer_questions(question_id)
        return render_template('new_answer.html', route=route, question_id=question_id,
                                                 question_to_render=question_to_render, )
    elif request.method == 'POST':
        answers = connection.import_data("sample_data/answer.csv")
        new_answer = {}
        new_answer['id'] = data_manager.get_id(answers)
        new_answer['submission_time'] = data_manager.get_unixtime()
        new_answer['vote_number'] = 0
        new_answer['question_id'] = question_id
        new_answer['message'] = request.form['new_answer']
        new_answer['image'] = None
        answers.append(new_answer)
        connection.export_data(answers, 'sample_data/answer.csv')
        return redirect(url_for("question", question_id=question_id))


@app.route("/add-question")
def add_question():
    return render_template('add-question.html')

# @app.route('/display_question', methods=['POST'])
# def display_question():
#     new_question = {}
#     counter = len(connection.import_data('sample_data/question.csv'))+1
#     if request.method == 'POST':
#         id = counter
#         new_question['id'] = str(id)
#         submission_time = data_manager.get_unixtime()
#         new_question['submission_time'] = submission_time
#         new_question['view_number'] = 0
#         new_question['vote_number'] = 0
#         title = request.form['title']
#         new_question['title'] = title
#         message = request.form['message']
#         new_question['message'] = message
#         image = request.form['image']
#         if image:
#             new_question['image'] = image
#         new_question['image'] = None
#
#         questions = connection.import_data('sample_data/question.csv')
#         questions.append(new_question)
#         connection.export_data(questions, 'sample_data/question.csv')
#         return render_template('/display_added_question.html', new_question=new_question)


@app.route("/question/<question_id>")
def question(question_id):
    route = url_for("post_new_answer", question_id=question_id)
    answers = connection.import_data("sample_data/answer.csv")
    question_to_render, answers_to_render = data_manager.get_answer_questions(question_id)
    return render_template('question.html', question_to_render=question_to_render,
                           answers_to_render=answers_to_render, route=route)

@app.route("/edit_question/<question_id>")
def edit_question(question_id):
    questions = connection.import_data("sample_data/question.csv")
    question_to_edit = {}
    for line in questions:
        if question_id == line['id']:
            question_to_edit = line
    return render_template('display_question_to_edit.html', question_to_edit=question_to_edit)


@app.route('/display_question', methods=['POST'])
def display_question():
    new_question = {}
    counter = len(connection.import_data('sample_data/question.csv'))+1
    if request.method == 'POST':
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
        image = request.form['image']
        if image:
            new_question['image'] = image
        new_question['image'] = None

        questions = connection.import_data('sample_data/question.csv')
        questions.append(new_question)
        connection.export_data(questions, 'sample_data/question.csv')
        return render_template('/display_added_question.html', new_question=new_question)





@app.route("/rewrite_one_question", methods=['GET', 'POST'])
def rewrite_one_question():
    edited_question = {}
    if request.method == 'POST':
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

        if request.form['image']:
            image = request.form['image']
            edited_question.update({'image': image})
        else:
            edited_question.update({'image': None})

        questions = connection.import_data('sample_data/question.csv')
        for quest in questions:
            index = int(quest['id'])
            if quest['id'] == edited_question['id']:
                questions[index - 1] = edited_question
        connection.export_data(questions, 'sample_data/question.csv')
        questions = connection.import_data('sample_data/question.csv')
        return render_template('list.html', questions=questions)




@app.route("/list", methods=['GET', 'POST'])
@app.route("/")
def list_page():
    questions = connection.import_data("sample_data/question.csv")
    answers = connection.import_data("sample_data/answer.csv")
    if request.method == 'POST':
        order_by = request.form.get('order_by')
        order_direction = request.form.get('order_direction')
        if order_by == 'Title' and order_direction == 'ascending':
            questions = sorted(questions, key=lambda questions: questions['title'])
        if order_by == 'Title' and order_direction == 'descending':
            questions = sorted(questions, key=lambda questions: questions['title'], reverse=True)
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



if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
