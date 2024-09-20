import websocket
import json

def on_message(ws, message):
    print(f"Received: {message}")

def on_open(ws):
    username = input("Enter your username: ")
    room = input("Enter room name: ")
    ws.send(json.dumps({'type': 'join', 'username': username, 'room': room}))

    while True:
        message = input("Enter message (or type 'exit' to leave): ")
        if message.lower() == 'exit':
            ws.send(json.dumps({'type': 'leave', 'username': username, 'room': room}))
            break
        ws.send(json.dumps({'room': room, 'username': username, 'message': message}))

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:5000/socket.io/?EIO=3&transport=websocket",
                                  on_message=on_message)
    ws.on_open = on_open
    ws.run_forever()
