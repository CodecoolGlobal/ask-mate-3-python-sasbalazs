from flask import Flask, render_template, request, redirect, url_for
import connection

app = Flask(__name__)


@app.route("/add-question")
def add_question():
    return render_template('add-question.html')


@app.route("/question/<question_id>")
def question(question_id):
    return render_template('question.html')


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
