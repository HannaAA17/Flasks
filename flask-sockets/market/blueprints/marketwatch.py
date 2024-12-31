from threading import Thread, Lock

from flask import Blueprint, render_template, jsonify, current_app

from ..models import COLUMNS, generate_data
from ..extensions import socketio #, db


bp = Blueprint('marketwatch', __name__, url_prefix='/marketwatch')


@bp.route('/')
def index():
    return render_template('marketwatch/index.html', title='Bootstrap Table', columns=COLUMNS)


@bp.route('/api')
def api():
    data = generate_data()
    return jsonify({'data': data})


thread_lock = Lock()

# Background thread for broadcasting updates
def broadcast_updates(app_context):
    app_context.push()
    while True:
        if current_app.STOP_BROADCAST:
            print('closed the thread')
            break  # Stop broadcasting if the flag is set

        # Fetch the latest data (replace this with your DB query)
        data = generate_data()
        print('generated data')
        # Broadcast data to all connected clients
        socketio.emit('generated_data', {'data': data})
        socketio.sleep(5)


# WebSocket connect event
@socketio.on('connect')
def handle_connect():
    with thread_lock:
        current_app.CONNECTION_COUNT += 1
        if current_app.CONNECTION_COUNT == 1:
            # Start broadcasting thread when the first client connects
            current_app.STOP_BROADCAST = False
            current_app.BROADCAST_THREAD = Thread(
                target=broadcast_updates, args=(current_app.app_context(),), daemon=True
            )
            current_app.BROADCAST_THREAD.start()

    print(f"Client connected. Total connections: {current_app.CONNECTION_COUNT}")


# WebSocket disconnect event
@socketio.on('disconnect')
def handle_disconnect():
    with thread_lock:
        current_app.CONNECTION_COUNT -= 1
        if current_app.CONNECTION_COUNT == 0:
            # Stop broadcasting when the last client disconnects
            current_app.STOP_BROADCAST = True

    print(f"Client disconnected. Total connections: {current_app.CONNECTION_COUNT}")

