from flask import g

import sqlite3
from werkzeug.security import generate_password_hash


def connect_db():
    sql = sqlite3.connect('./db/questions.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def create_user(form):
    db = get_db()

    hashed_pass = generate_password_hash(
        form['password'], method='scrypt:32768:8:1'
    )

    db.execute(
        'INSERT INTO users '
        '(name, password, expert, admin) '
        'VALUES (?, ?, ?, ?)',
        [form['name'], hashed_pass, False, False]
    )
    db.commit()

    return True


def find_user(name, by='name'):
    db = get_db()
    user = db.execute(f'SELECT * FROM users WHERE {by}=(?)', [name]).fetchone()
    return user


def find_all_users(filter_text=''):
    db = get_db()
    users = db.execute(f'SELECT * FROM users {filter_text}').fetchall()
    return users


def get_current_user(session):
    if 'user' in session:
        return find_user(session['user'])
    else:
        return None


def toggle_expert(user_id):
    user = find_user(user_id, by='id')
    new_expert_value = [1, 0][user['expert']]
    
    db = get_db()
    db.execute('UPDATE users SET expert=(?) WHERE id=(?)', [new_expert_value, user_id])
    db.commit()
    
    return None


def create_question(user_id, form):
    db = get_db()

    db.execute(
        'INSERT INTO questions '
        '(question_text, asked_by_id, expert_id) '
        'VALUES (?, ?, ?)',
        [form['question_text'], user_id, form['expert_id']]
    )
    db.commit()

    return None


def find_all_questions(filter_text=''):
    db = get_db()
    questions = db.execute('''
        SELECT 
            q.id, q.question_text, q.answer_text, 
            q.asked_by_id, u.name as asked_by_name, 
            q.expert_id, uu.name as expert_name 
        FROM questions q
        LEFT JOIN users u
            ON q.asked_by_id = u.id
        LEFT JOIN users uu
            ON q.expert_id = uu.id
        {} 
        '''.format(filter_text)
    ).fetchall()
    return questions


def add_answer(question_id, answer_text):
    db = get_db()
    db.execute('UPDATE questions SET answer_text=(?) WHERE id=(?)', [answer_text, question_id])
    db.commit()
    return None

# update users set admin='1' where id=1;
# alter table questions rename column 'export_id' to 'expert_id';
'''
select 
	q.id, q.question_text, q.answer_text, 
	q.asked_by_id,u.name as asked_by_name, 
	q.expert_id, uu.name as expert_name 
from questions q
left JOIN users u
	on q.asked_by_id = u.id
left join users uu
	on q.expert_id = uu.id
'''