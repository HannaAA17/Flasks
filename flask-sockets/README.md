# Flask Market Watch Application

This is a Flask application that provides real-time market data updates using WebSockets.

## Features

- Real-time data updates using Flask-SocketIO
- Background thread for broadcasting updates to connected clients
- REST API endpoint to fetch the latest data
- Bootstrap table for displaying data

## Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start a local Redis server (if you are on Linux or Mac, execute  to install and launch a private copy).

2. Set environment variables for Flask:

    ```sh
    export FLASK_APP=app.py
    export FLASK_ENV=development
    ```

3. Run the Flask application:

    ```sh
    flask run
    ```

4. Open a new terminal window and start the SocketIO server:

    ```sh
    flask run --host=0.0.0.0 --port=5000
    ```

5. Open your web browser and go to `http://localhost:5000/`.

## API Endpoints

- `/marketwatch/`: Renders the main page with the Bootstrap table.
- `/marketwatch/api`: Returns the latest data in JSON format.

## WebSocket Events

- `connect`: Triggered when a client connects. Starts the broadcasting thread if it's the first connection.
- `disconnect`: Triggered when a client disconnects. Stops the broadcasting thread if it's the last connection.
- `generated_data`: Broadcasts the latest data to all connected clients.

## License

This project is licensed under the MIT License.