var socket = io()
var log = document.getElementById('log')
var emitForm = document.getElementById('attack')
var leaveForm = document.getElementById('leave')
var emitData = new FormData(emitForm)
// var emitData = new FormData(document.getElementById('emit_data'))
//
emitForm.addEventListener('submit', emitAction)

function emitAction(event) {
    event.preventDefault();
    console.log("Attack")
    socket.emit('attack')
    return false
}

// leaveForm.addEventListener('submit', leaveAction)

// function leaveAction(event) {
//     socket.emit('leave')
//     return false
// }

socket.on('attack_response', function (msg, callback) {
    // log.textContent += msg.count
    var br = document.createElement("br");
    log.appendChild(br);
    console.log(typeof(msg.data))
    log.innerHTML += '\r\n'
    // log.innerHTML += '<br>'
    // log.innerHTML += '<br />'
    if (msg.data)
        log.textContent += "attack success"
    else
        log.textContent += "attack fail"

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

