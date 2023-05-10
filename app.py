from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'hw13.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()

def delete_db(query, args=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            flash('You were logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username/password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash('You need to log in first', 'danger')
        return redirect(url_for('login'))
    students = query_db('SELECT * FROM students')
    quizzes = query_db('SELECT * FROM quizzes')
    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        flash('You need to log in first', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        insert_db('INSERT INTO students (first_name, last_name) VALUES (?, ?)', [first_name, last_name])
        flash('Student added successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        flash('You need to log in first', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        quiz_date = request.form['quiz_date']
        insert_db('INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)', [subject, num_questions, quiz_date])
        flash('Quiz added successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_quiz.html')

@app.route('/student/<int:id>')
def student_results(id):
    if not session.get('logged_in'):
        flash('You need to log in first', 'danger')
        return redirect(url_for('login'))
    results = query_db('''SELECT results.quiz_id, quizzes.subject, quizzes.quiz_date, results.score
                          FROM results
                          INNER JOIN quizzes ON results                          .quiz_id = quizzes.id
                          WHERE results.student_id = ?''', [id])

    return render_template('student_results.html', results=results)

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        flash('You need to log in first', 'danger')
        return redirect(url_for('login'))
    students = query_db('SELECT * FROM students')
    quizzes = query_db('SELECT * FROM quizzes')
    if request.method == 'POST':
        student_id = request.form['student']
        quiz_id = request.form['quiz']
        score = request.form['score']
        insert_db('INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)', [student_id, quiz_id, score])
        flash('Quiz result added successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_result.html', students=students, quizzes=quizzes)

if __name__ == '__main__':
    app.run(debug=True)

