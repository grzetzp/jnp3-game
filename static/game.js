var socket = io()
var logAttack = document.getElementById('log_attack')
var logEcho = document.getElementById('log_echo')
var attackForm = document.getElementById('attack')
var leaveForm = document.getElementById('leave')
var emitData = new FormData(attackForm)
var emitForm = document.getElementById('emit')
var joinForm = document.getElementById('join_game')
// var log = document.getElementById('log')

// var emitData = new FormData(document.getElementById('emit_data'))
//
attackForm.addEventListener('submit', attackAction)

function attackAction(event) {
    event.preventDefault();
    console.log("Attack")
    socket.emit('attack')
    return false
}

emitForm.addEventListener('submit', emitAction)

function emitAction(event) {
    event.preventDefault();
    console.log("Submit " + emitForm['emit_data'].value)
    socket.emit('my_event', {data: emitForm['emit_data'].value})
    // return false
}

// joinForm.addEventListener('submit', joinGame)

// function joinGame(event) {
//     // event.preventDefault();
//     console.log("Player " + joinForm['username'].value + " joining.")
//     socket.emit('join_game', {data: joinForm['username'].value})
// }

socket.on('my_response', function (msg, callback) {
    // logEcho.textContent += msg.count
    var br = document.createElement("br");
    logEcho.appendChild(br);
    logEcho.innerHTML += '\r\n'
    logEcho.innerHTML += '<br>'
    logEcho.innerHTML += '<br />'
    logEcho.textContent += msg.data

    if (callback) {
        callback()
    }
})

socket.on('connect', function () {
    console.log("I\'m connected!")
    socket.emit('my_event', {data: "I\'m connected!"})
})


// leaveForm.addEventListener('submit', leaveAction)

// function leaveAction(event) {
//     socket.emit('leave')
//     return false
// }

socket.on('attack_response', function (msg, callback) {
    // logAttack.textContent += msg.count
    var br = document.createElement("br");
    logAttack.appendChild(br);
    console.log(typeof(msg.data))
    logAttack.innerHTML += '\r\n'
    // logAttack.innerHTML += '<br>'
    // logAttack.innerHTML += '<br />'
    if (msg.data)
        logAttack.textContent += "attack success"
    else
        logAttack.textContent += "attack fail"

    if (callback) {
        callback()
    }
})

socket.on('player_joined', function () {

})

socket.on('connect', function () {
    console.log("I\'m connected!")
    socket.emit('my_event', {data: "I\'m connected!"})
})