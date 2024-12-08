from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orginate')
def orginate():
    socketio.emit('server orginated', 'Something happened on the server!')
    return '<h1>Sent!</h1>'

@app.route('/close/<room>')
def close(room):
    close_room(room, namespace='/private')
    return '<h1>Room closed!</h1>'

@socketio.on('message from user', namespace='/messages')
def receive_message_from_user(message):
    print('USER MESSAGE: {}'.format(message))
    emit('from flask', message.upper(), broadcast=True)

@socketio.on('username', namespace='/private')
def receive_username(username):
    users[username] = request.sid
    #users.append({username : request.sid})
    #print(users)
    print('Username added!')

@socketio.on('private_message', namespace='/private')
def private_message(payload):
    recipient_session_id = users[payload['username']]
    message = payload['message']

    emit('new_private_message', message, room=recipient_session_id)

@socketio.on('join_room', namespace='/private')
def handle_join_room(room):
    join_room(room)
    emit('room_message', 'a new user has joined', room=room)

@socketio.on('leave_the_room', namespace='/private')
def handle_leave_room(room):
    leave_room(room)
    emit('room_message', 'a user has left the room', room=room)

@socketio.on('connect', namespace='/private')
def on_connect():
    print('NEW CONNECTION ESTABLISHED!')

@socketio.on('disconnect', namespace='/private')
def on_disconnect():
    print('CONNECTION ENDED!')

@socketio.on('disconnect_me', namespace='/private')
def disconnect_me(message):
    disconnect()

'''
@socketio.on('message')
def receive_message(message):
    print('########: {}'.format(message))
    send('This is a message from Flask.')

@socketio.on('custom event')
def receive_custom_event(message):
    print('THE CUSTOM MESSAGE IS: {}'.format(message['name']))
    emit('from flask', {'extension' : 'Flask-SocketIO'}, json=True)

'''

if __name__ == '__main__':
    socketio.run(app)