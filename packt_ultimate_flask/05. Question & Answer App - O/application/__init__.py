from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'random text'


from application import routes