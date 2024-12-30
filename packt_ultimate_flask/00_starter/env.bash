set FLASK_APP=myapp
set FLASK_DEBUG=1

py -m flask run


py -m flask db init
py -m flask db migrate
py -m flask db upgrade
