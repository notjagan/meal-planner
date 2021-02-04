function handshake() {
    const socket = new WebSocket('wss://10.108.99.175:61453');

    socket.addEventListener('open', function (event) {
        socket.send('client');
    });

    socket.addEventListener('message', function (event) {
        console.assert(event.data == 'server');
    });
}
