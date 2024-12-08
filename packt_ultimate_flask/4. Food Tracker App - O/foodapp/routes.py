import datetime

from flask import render_template, request

from foodapp import app, get_db


# ============================================================
def pretty_date(date):
    return (
        datetime.datetime
        .strptime(str(date), '%Y%m%d')
        .strftime('%B %d, %Y')
    )
    

# ============================================================


@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    
    # add new date
    if request.method == 'POST':
        date_str = request.form['date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        date_db = date.strftime('%Y%m%d')
        # date_pretty = date.strftime('%B %d, %Y')

        db.execute('INSERT INTO log_date (entry_date) VALUES (?)', [date_db])
        db.commit()
    
    cur = db.execute(
        'SELECT log_date.entry_date,'
        ' SUM(food.protein) AS protein, SUM(food.carbohydrates) AS carbohydrates,'
        ' SUM(food.fat) AS fat, SUM(food.calories) AS calories'
        ' FROM log_date'
        ' left JOIN food_date ON food_date.log_date_id = log_date.id'
        ' left JOIN food ON food.id = food_date.food_id'
        ' GROUP BY log_date.id ORDER BY log_date.entry_date DESC'
    )    
    results = [
        {
            'entry_date': str(row['entry_date']),
            'pretty_entry_date': pretty_date(row['entry_date']),
            'protein': row['protein'],
            'carbohydrates': row['carbohydrates'],
            'fat': row['fat'],
            'calories': row['calories'],
        }
        for row in cur.fetchall()
    ]
    
    return render_template('index.html', results=results)


@app.route('/view/<date>', methods=['GET', 'POST']) #20170520
def view(date):
    
    db = get_db()

    # today
    cur = db.execute('SELECT id, entry_date FROM log_date WHERE entry_date = ?', (date,))    
    date_result = cur.fetchone()

    today = {
        'entry_date_id': date_result['id'],
        'entry_date': str(date_result['entry_date']),
        'pretty_entry_date': pretty_date(date_result['entry_date']),
    }

    # available foods 
    cur = db.execute('SELECT id, name FROM food')
    food_results = cur.fetchall()
    valid_foods = {str(food['id']) for food in food_results}

    if request.method == 'POST':
        food_id = request.form['food-select']
        if food_id in valid_foods:
            db.execute('INSERT INTO food_date (food_id, log_date_id) VALUES (?, ?)', [food_id, today['entry_date_id']])
            db.commit()
    
    
    # day foods
    cur = db.execute(
        'SELECT food.id, food.name, food.protein, food.carbohydrates, food.fat, food.calories FROM food_date'
        ' JOIN food ON food_date.food_id = food.id'
        ' WHERE food_date.log_date_id = ?'
        ' ORDER BY food.id', [today['entry_date_id']]
    )
    today_foods = cur.fetchall()

    # day totals
    foods_totals = {
        'protein': 0,
        'carbohydrates': 0,
        'fat': 0,
        'calories': 0,
    }
    
    for food in today_foods:
        foods_totals['protein'] += food['protein']
        foods_totals['carbohydrates'] += food['carbohydrates']
        foods_totals['fat'] += food['fat']
        foods_totals['calories'] += food['calories']


    return render_template('day.html', today=today, food_results=food_results, today_foods=today_foods, foods_totals=foods_totals)


@app.route('/food', methods=['GET', 'POST'])
def add_food():

    db = get_db()

    if request.method == 'POST':
        food_name = request.form['food-name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])

        calories = (protein + carbohydrates)*4 + fat*9

        db.execute(
            'INSERT INTO food (name, protein, carbohydrates, fat, calories)'
            ' VALUES (?, ?, ?, ?, ?)',
            [food_name, protein, carbohydrates, fat, calories]
        )
        db.commit()
        
        return 'Success!!'
    
    
    cur = db.execute('SELECT name, protein, carbohydrates, fat, calories FROM food')    
    results = cur.fetchall()
    return render_template('add_food.html', results=results)

# ============================================================
