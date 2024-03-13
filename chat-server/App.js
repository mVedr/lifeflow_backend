import express from 'express';
import { Server } from 'socket.io';
import { createServer } from 'http';
import cors from 'cors';

const app = express();
app.use(cors());

const port = 3000;

const server = createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST'],
    credentials: true,
  },
});

app.get('/', (req, res) => {
  res.send('Hello World');
});

io.on('connect', (socket) => {
  console.log('connected', socket.id);
  socket.emit('message', 'Welcome to the chat');

  socket.on('message', (msg) => {
    console.log('Received message:', msg);
    // Broadcast the message to all connected clients
    io.emit('message', msg);
  });
});

server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
