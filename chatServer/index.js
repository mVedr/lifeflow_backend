const express=require('express');
const app =express();
const http = require('http').Server(app);
const cors=require('cors');
const socketio=require('socket.io')(http,{
    cors:{
        origin:"*",
    }
})
const port=4000;
app.use(express.urlencoded({extended:true}));
app.use(express.json());
app.use(cors());
// socketio.use((socket,next)=>{
//     const username=socket.handshake.auth.username;
//     if(!username){
//         return next(new Error("invalid username"))

//     }
//     socket.username=username;
//     next();
// })
socketio.on('connection',(socket)=>{

    console.log(`${socket.id}user connected`);

    socket.on('personal',({
        senderEmail,
        message,
      })=>{
        console.log(senderEmail,message);
        socketio.to(socket.id).emit('personal',{message});
        
    })
})


app.get('/api',(req,res)=>{
    console.log(req,res);
})
http.listen(port,()=>{
    console.log(`server listening on port ${port}`)
})
