function handshake() {
    const socket = new WebSocket('ws://localhost:61453');

    socket.addEventListener('open', function (event) {
        socket.send('client');
    });

    socket.addEventListener('message', function (event) {
        console.assert(event.data == 'server');
    });
}
