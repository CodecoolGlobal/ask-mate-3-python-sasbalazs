from flask import Flask, render_template, request, redirect, url_for
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
        new_answer['image'] = 0
        answers.append(new_answer)
        connection.export_data(answers, 'sample_data/answer.csv')
        return redirect(url_for("question", question_id=question_id))


@app.route("/add-question")
def add_question():
    return render_template('add-question.html')


@app.route("/question/<question_id>")
def question(question_id):
    route = url_for("post_new_answer", question_id=question_id)
    question_to_render, answers_to_render = data_manager.get_answer_questions(question_id)
    return render_template('question.html', question_to_render=question_to_render,
                           answers_to_render=answers_to_render, route=route)


@app.route("/list")
@app.route("/")
def list_page():
    questions = connection.import_data("sample_data/question.csv")
    answers = connection.import_data("sample_data/answer.csv")
    return render_template('list.html', questions=questions, answers=answers)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
