// server.js

const WebSocket = require('ws');
const http = require('http');
const express = require('express');
const cors = require('cors');
const path = require('path');

// Set up the Express server
const app = express();
app.use(cors()); // Enable CORS for all origins
app.use(express.static(path.join(__dirname, 'public')));

const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const rooms = {}; // To keep track of rooms and their clients

wss.on('connection', (ws, req) => {
    const url = new URL(req.headers.origin);
    const roomName = url.pathname.split('/')[1] || 'default';

    if (!rooms[roomName]) {
        rooms[roomName] = new Set();
    }

    rooms[roomName].add(ws);
    console.log(`User connected to room: ${roomName}`);

    ws.on('message', message => {
        try {
            const data = JSON.parse(message);
            if (data.type === 'edit' || data.type === 'delete') {
                // Handle edit and delete
                rooms[roomName].forEach(client => {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify(data));
                    }
                });
            } else {
                // Broadcast new messages
                rooms[roomName].forEach(client => {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(message);
                    }
                });
            }
        } catch (e) {
            console.error('Invalid message format:', message);
        }
    });

    ws.on('close', () => {
        rooms[roomName].delete(ws);
        console.log(`User disconnected from room: ${roomName}`);
        if (rooms[roomName].size === 0) {
            delete rooms[roomName];
        }
    });
});

server.listen(8080, () => {
    console.log('Server is running on http://localhost:8080');
});
