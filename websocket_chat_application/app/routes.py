from flask import jsonify
from flask_socketio import join_room, leave_room, emit
from app import app, socketio

# Store active chat rooms and their participants
rooms = {}

@app.route('/')
def index():
    return jsonify(message="Welcome to the WebSocket Chat Application!")

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    
    # Check if room exists; if not, create it
    if room not in rooms:
        rooms[room] = []
    
    # Add user to the room
    if username not in rooms[room]:
        rooms[room].append(username)
    
    join_room(room)  # Use SocketIO to manage room joining
    emit('user_joined', {'username': username, 'room': room}, room=room)

    # Notify all users in the room
    emit('message', {'username': 'Server', 'message': f'{username} has joined the room.'}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    
    # Check if the room exists
    if room in rooms:
        emit('message', data, room=room)  # Broadcast message to the room

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    
    if room in rooms and username in rooms[room]:
        rooms[room].remove(username)  # Remove user from the room
        leave_room(room)
        emit('user_left', {'username': username, 'room': room}, room=room)
        emit('message', {'username': 'Server', 'message': f'{username} has left the room.'}, room=room)

@socketio.on('disconnect')
def handle_disconnect():
    print('A user has disconnected')
