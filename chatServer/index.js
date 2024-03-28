const express = require('express');
const app = express();
const http = require('http').Server(app);
const cors = require('cors');
const socketio = require('socket.io')(http, {
    cors: {
        origin: "*",
    }
});
const port = 4000;
const userSocketMap = {};

app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

socketio.on('connection', (socket) => {
    socket.on('register', (email) => {
        console.log(`${email} connected`);
        userSocketMap[email] = socket.id; 
    });

    socket.on('disconnect', () => {
        Object.keys(userSocketMap).forEach((email) => {
            if (userSocketMap[email] === socket.id) {
                delete userSocketMap[email];
                console.log(`${email} disconnected`);
            }
        });
    });

    socket.on('sendToUser', ({ recipientEmail, message }) => {
        const recipientSocketId = userSocketMap[recipientEmail];
        if (recipientSocketId) {
            console.log(`Sending message from server to ${recipientEmail}`);
            socketio.to(recipientSocketId).emit('personal', { senderEmail: 'server', message }); 
        }
    });
});

app.get('/api', (req, res) => {
    res.send('API endpoint');
});

http.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
