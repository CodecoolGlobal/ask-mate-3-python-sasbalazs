from flask import Flask, render_template, request, redirect, url_for
import connection
import data_manager

app = Flask(__name__)


@app.route("/add-question")
def add_question():
    return render_template('add-question.html')

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
