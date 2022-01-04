var socket = io()
var log = document.getElementById('log')
var emitForm = document.getElementById('emit')
var joinForm = document.getElementById('join_game')
// var emitData = new FormData(emitForm)
// var emitData = new FormData(document.getElementById('emit_data'))
//
emitForm.addEventListener('submit', emitAction)

function emitAction(event) {
    event.preventDefault();
    console.log("Submit " + emitForm['emit_data'].value)
    socket.emit('my_event', {data: emitForm['emit_data'].value})
    // return false
}

joinForm.addEventListener('submit', joinGame)

function joinGame(event) {
    // event.preventDefault();
    console.log("Player " + joinForm['username'].value + " joining.")
    socket.emit('join_game', {data: joinForm['username'].value})
}

socket.on('my_response', function (msg, callback) {
    // log.textContent += msg.count
    var br = document.createElement("br");
    log.appendChild(br);
    log.innerHTML += '\r\n'
    log.innerHTML += '<br>'
    log.innerHTML += '<br />'
    log.textContent += msg.data

    if (callback) {
        callback()
    }
})

socket.on('connect', function () {
    console.log("I\'m connected!")
    socket.emit('my_event', {data: "I\'m connected!"})
})
