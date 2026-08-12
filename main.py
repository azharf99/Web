from flask import Flask, session, render_template, request
from db import show, show_questions_by_quiz_id, get_correct_answer
from random import shuffle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'
def start_quiz(quiz_id):
    '''creates the desired values ​​in the session dictionary'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def shuffle_options(data):
    new_data = list()
    for question in data:
        id, question, o1, o2, o3, o4 = question
        options = [o1, o2, o3, o4]
        shuffle(options)
        o1, o2, o3, o4 = options
        new_data.append((id, question, o1, o2, o3, o4))
    return new_data

@app.route('/')
def index():
    start_quiz(-1)
    data = show('quiz')
    return render_template('index.html', data=data)

@app.route('/quiz')
def quiz_management():
    data = show('quiz')
    return render_template('index.html', data=data)

@app.route('/test')
@app.route('/test/<id>')
def test(id=None):
    keyword = request.args.get('quiz_id', type=int)
    if keyword:
        start_quiz(keyword)
        data = show_questions_by_quiz_id(keyword)
        data = shuffle_options(data)
        return render_template('test.html', data=data)
    elif id:
        start_quiz(int(id))
        data = show_questions_by_quiz_id(id)
        return render_template('test.html', data=data)
    return 'Halaman Test'

@app.route('/result', methods=['POST', 'GET'])
def result():
    result = 0
    total_question = 0
    if request.method == 'POST':
        for id, answer in request.form.items():
            session['last_question'] = id
            session['answers'] = answer
            result += get_correct_answer(int(id), answer)
            total_question += 1

        session['total'] = result
        return render_template('result.html', nilai=result, akurasi=(result/total_question)*100, jumlah_soal=total_question)
    return 'Halaman Hasil'

app.run()