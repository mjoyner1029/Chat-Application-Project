from flask import jsonify
from app import app, socketio

rooms = {}

@app.route('/')
def index():
    return jsonify(message="Welcome to the WebSocket Chat Application!")

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    if room not in rooms:
        rooms[room] = []
    rooms[room].append(username)
    socketio.emit('user_joined', {'username': username, 'room': room}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    socketio.emit('message', data, room=room)

@socketio.on('disconnect')
def handle_disconnect():
    pass
