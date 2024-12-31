from market import create_app
from market.extensions import socketio

if __name__ == '__main__':
    app = create_app()

    # Run the Flask app with SocketIO
    socketio.run(app, debug=False)