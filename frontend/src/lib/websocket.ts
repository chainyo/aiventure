let socket: WebSocket | null = null;

export function initializeSocket() {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const token = user.token;

  if (!token) {
    console.error('No token found. Unable to initialize WebSocket.');
    return;
  }

  socket = new WebSocket(`ws://your-websocket-url?token=${token}`);

  socket.onopen = () => {
    console.log('WebSocket connection established');
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received data:', data);
    // Handle the received data as needed
  };

  socket.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  socket.onclose = () => {
    console.log('WebSocket connection closed');
  };
}

export function closeSocket() {
  if (socket) {
    socket.close();
  }
}

export function getPlayerData() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: 'get_player_data' }));
  } else {
    console.error('WebSocket is not open. Unable to get player data.');
  }
}

