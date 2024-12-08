set FLASK_APP=myapp
set FLASK_DEBUG=1

flask db migrate
flask db upgrade
