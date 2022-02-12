var socket = io()
var log = document.getElementById('log')
var leaveForm = document.getElementById('leave')

leaveForm.addEventListener('submit', emitAction)

var room = getRandomHash();
var rating_range = 10;


(function(){
    console.log("HUHUHUHUHUHUHUHUHUH");
    log.innerHTML += "<p> Checking for games in rating range" + rating_range  + "</p>"
    socket.emit('check_now', {'range': rating_range, 'room_log': log.innerHTML});
    rating_range += 10;
    setTimeout(arguments.callee, 10000);
})();


function emitAction(event) {
    event.preventDefault();
    console.log("Leave")
    socket.emit('leave', {'room': room});
    return false
}

function getRandomHash() {
    var length = 20;
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() *
 charactersLength));
   }
   return result;
}

socket.on('connect', function () {
    console.log("I\'m connected! room nr", room);
    document.getElementById("roomID").innerHTML = room;

    socket.emit('join', {'room': room});
})

socket.on('found', function (data) {
    console.log("found");
    window.location = data['url'];
})