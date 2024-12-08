from flask import Flask 
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.hushmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'anthony@prettyprinted.com'
app.config['MAIL_PASSWORD'] = ';kAO3MJgCdByHu'
app.config['MAIL_DEFAULT_SENDER'] = ('Anthony from PrettyPrinted', 'anthony@prettyprinted.com')
app.config['MAIL_MAX_EMAILS'] = None
#app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

#mail = Mail()
#mail.init_app(app)

@app.route('/')
def index():
    msg = Message('Hey There', recipients=['anthony@anthonyherbert.com'])
    #msg.body = 'Here is the body!'
    msg.html = '<b>This is a test email sent from Anthony\'s app. You don\'t have to reply.</b>'

    with app.open_resource('cat.jpg') as cat:
        msg.attach('cat.jpg', 'image/jpeg', cat.read())

    mail.send(msg)

    msg = Message(
            subject = '',
            recipients = [],
            body = '',
            html = '',
            sender = '',
            cc = [],
            bcc = [],
            attachments = [],
            reply_to = [],
            date = 'date',
            charset = '',
            extra_headers = {'': ''},
            mail_options = [],
            rcpt_options = []
        )

    return 'Message has been sent!'

@app.route('/bulk')
def bulk():
    users = [{'name' : 'Anthony', 'email' : 'email@email.com'}]

    with mail.connect() as conn:
        for user in users:
            msg = Message('Bulk!', recipients=[user.email])
            msg.body = 'Hey There'
            conn.send(msg)

if __name__ == '__main__':
    app.run()