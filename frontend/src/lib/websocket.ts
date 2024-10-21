import { io, Socket } from 'socket.io-client';

let socket: Socket | null = null;

export function initializeSocket() {
  socket = io('http://localhost:5150');

  socket.on('connect', () => {
    console.log('Socket.IO connection established');
  });

  socket.on('message', (data) => {
    console.log('Received data:', data);
    // Handle the received data as needed
  });

  socket.on('connect_error', (error) => {
    console.error('Socket.IO connection error:', error);
  });

  socket.on('disconnect', (reason) => {
    console.log('Socket.IO connection closed:', reason);
  });
}

export function closeSocket() {
  if (socket) {
    socket.disconnect();
  }
}

export function getPlayerData() {
  if (socket && socket.connected) {
    socket.emit('get_player_data');
  } else {
    console.error('Socket.IO is not connected. Unable to get player data.');
  }
}
