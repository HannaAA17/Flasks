from flask import render_template, redirect, url_for, request, session

from werkzeug.security import check_password_hash

from application import app
# from application.database import close_db, create_user, find_user, find_all_users, get_current_user, toggle_expert
import application.database as db_client


def check_permission(user, allowed='user'):
    if (not user) & (allowed=='guest'):
        return True
    elif (not user):
        return False
    elif allowed=='admin':
        return user['admin']
    elif allowed=='expert':
        return user['expert']
    elif allowed=='user':
        return (not user['admin']) & (not user['expert'])


@app.teardown_appcontext
def teardown(error):
    db_client.close_db(error)


@app.route('/')
def index():
    user = db_client.get_current_user(session)

    questions = db_client.find_all_questions('WHERE q.answer_text IS NOT NULL')
    return render_template('home.html', user=user, questions=questions)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if db_client.find_all_users('WHERE name="{}"'.format(request.form['name'])):
            return 'already exists'
        else:
            # create user
            db_client.create_user(request.form)
            session['user'] = request.form['name']

    user = db_client.get_current_user(session)
    if not check_permission(user, 'guest'):
        return redirect(url_for('index'))

    return render_template('register.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get the user data from the database
        user_result = db_client.find_user(request.form['name'])

        # check if the name and pass match
        if not user_result:
            return 'name not registered, please register first'
        elif check_password_hash(user_result['password'], request.form['password']):
            # create session
            session['user'] = user_result['name']
        else:
            return 'password not correct'

    user = db_client.get_current_user(session)
    if not check_permission(user, 'guest'):
        return redirect(url_for('index'))

    return render_template('login.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    user = db_client.get_current_user(session)
    if not check_permission(user, 'user'):
        return 'you dont have permission to enter this page'
    
    if request.method == 'POST':
        db_client.create_question(user['id'], request.form)
        return redirect(url_for('index'))

    experts_data = db_client.find_all_users('WHERE expert=1')
    experts_data.sort(key=lambda x: x['name'])
    return render_template('ask.html', user=user, experts_data=experts_data)


@app.route('/users')
def users():
    user = db_client.get_current_user(session)
    if not check_permission(user, 'admin'):
        return 'you dont have permission to enter this page'

    users_data = db_client.find_all_users()
    users_data.sort(key=lambda x: x['name'])

    return render_template('users.html', user=user, users_data=users_data)


@app.route('/promote/<user_id>')
def promote(user_id):
    user = db_client.get_current_user(session)
    if not check_permission(user, 'admin'):
        return 'you dont have permission for this action'
    
    db_client.toggle_expert(user_id)
    return redirect(url_for('users'))


@app.route('/unanswered')
def unanswered():
    user = db_client.get_current_user(session)
    if not check_permission(user, 'expert'):
        return 'you dont have permission to enter this page'
    
    questions = db_client.find_all_questions(
        'WHERE answer_text IS NULL AND expert_id={}'.format(user['id'])
    )
    return render_template('unanswered.html', user=user, questions=questions)


@app.route('/question/<question_id>')
def question(question_id):
    user = db_client.get_current_user(session)
    question = db_client.find_all_questions(
        'WHERE q.id={}'.format(question_id)
    )[0]
    return render_template('question.html', user=user, question=question)


@app.route('/answer/<question_id>', methods=['GET', 'POST'])
def answer(question_id):
    if request.method == 'POST':
        db_client.add_answer(question_id, request.form['answer_text'])
        return redirect(url_for('unanswered'))

    user = db_client.get_current_user(session)
    if not check_permission(user, 'expert'):
        return 'you dont have permission to enter this page'

    question = db_client.find_all_questions(
        'WHERE q.id={}'.format(question_id)
    )[0]

    return render_template('answer.html', user=user, question=question)
