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

    return render_template('question.html', questions=questions, answers=answers, question_to_render=question_to_render,
                           answers_to_render=answers_to_render)


@app.route("/list", methods=['GET', 'POST'])
@app.route("/")
def list_page():
    questions = connection.import_data("sample_data/question.csv")
    answers = connection.import_data("sample_data/answer.csv")
    if request.method == 'POST':
        order_by = request.form.get('order_by')
        order_direction = request.form.get('order_direction')
        print(order_by)
        if order_by == 'Title' and order_direction == 'ascending':
            questions = sorted(questions, key=lambda questions: questions['title'])
        if order_by == 'Title' and order_direction == 'descending':
            questions = sorted(questions, key=lambda questions: questions['title'], reverse=True)
        if order_by == 'View number' and order_direction == 'ascending':
            questions = sorted(questions, key=lambda questions: int(questions['view_number']))
        if order_by == 'View number' and order_direction == 'descending':
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
