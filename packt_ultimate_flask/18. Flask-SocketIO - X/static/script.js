$(document).ready(function () {

    const SOCKET = io.connect('http://127.0.0.1:5000');
    const SOCKET_MESSAGES = io('http://127.0.0.1:5000/messages')
    const PRIVATE_SOCKET = io('http://127.0.0.1:5000/private')


    $('#send').on('click', function () {
        var message = $('#message').val();s
        SOCKET_MESSAGES.emit('message from user', message);

    });

    $('#send_username').on('click', function () {
        PRIVATE_SOCKET.emit('username', $('#username').val());
    });

    $('#send_private_message').on('click', function () {
        var recipient = $('#send_to_username').val();
        var message_to_send = $('#private_message').val();
        PRIVATE_SOCKET.emit('private_message', { 'username': recipient, 'message': message_to_send });
    });

    $('#join_room').on('click', function () {
        var room = $('#room_to_join').val();
        PRIVATE_SOCKET.emit('join_room', room);
    });

    $('#leave_room').on('click', function () {
        var room = $('#room_to_join').val();
        PRIVATE_SOCKET.emit('leave_the_room', room);
    });

    $('#disconnect').on('click', function () {
        PRIVATE_SOCKET.emit('disconnect_me', 'disconnect');
    });


    SOCKET.on('server orginated', function (msg) {
        alert(msg);
    });

    SOCKET_MESSAGES.on('from flask', function (msg) {
        alert(msg);
    });

    PRIVATE_SOCKET.on('new_private_message', function (msg) {
        alert(msg);
    });

    PRIVATE_SOCKET.on('room_message', function (msg) {
        alert(msg);
    });

    /*

    socket.on('connect', function() {
    
        socket.send('I am now connected!');

        socket.emit('custom event', {'name' : 'Anthony'});

        socket.on('from flask', function(msg) {
            alert(msg['extension']);
        });

        socket.on('message', function(msg) {
            alert(msg);
        });
        
    });

    */

});