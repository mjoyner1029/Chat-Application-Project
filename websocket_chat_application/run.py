from app import socketio, app

if __name__ == '__main__':
    socketio.run(app, debug=True)  # Run the Flask app with SocketIO
