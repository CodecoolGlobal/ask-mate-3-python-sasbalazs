from flask import Flask, render_template, request, redirect, url_for
import connection

app = Flask(__name__)


@app.route("/add-question")
def add_question():
    return render_template('add-question.html')


@app.route("/question/<question_id>")
def question(question_id):
    questions = connection.import_data("sample_data/question.csv")
    answers = connection.import_data("sample_data/answer.csv")
    question_to_render = {}
    answers_to_render = {}
    for line in questions:
        if question_id == line['id']:
            question_to_render = line
            for answer in answers:
                if question_id == answer['question_id']:
                    answers_to_render = answer

    return render_template('question.html', questions=questions, answers=answers, question_to_render=question_to_render, answers_to_render=answers_to_render)

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
