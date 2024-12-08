from flask import Flask, render_template, request
from flask_babel import Babel, get_locale, format_date, format_datetime, gettext
from datetime import date, datetime

app = Flask(__name__)
babel = Babel(app)

@babel.localeselector
def localeselector():
    #return 'en_US'
    return request.accept_languages.best_match(['en_US', 'es_ES'])

@app.route('/')
def index():
    d = date(2011, 1, 8)
    dt = datetime(2010, 4, 9, 21, 13)

    local_date = format(d)
    local_datetime = format_datetime(dt)

    anthony = gettext('Anthony')
    python = gettext('Python')

    return render_template('index.html', locale=get_locale(), local_date=local_date, local_datetime=local_datetime,
        anthony=anthony, python=python)

if __name__ == '__main__':
    app.run(debug=True)