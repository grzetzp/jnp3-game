var socket = io()
var log = document.getElementById('log')
var leaveForm = document.getElementById('leave')

leaveForm.addEventListener('submit', emitAction)

var room = getRandomHash();
var rating_range = 10;


(function(){
    log.innerHTML += "<p> Checking for games in rating range of " + rating_range  + "...</p>"
    socket.emit('check_now', {'range': rating_range, 'room_log': log.innerHTML});
    rating_range += 10;
    setTimeout(arguments.callee, 10000);
})();

(function () {
    console.log("I\'m connected! room nr", room);
    document.getElementById("roomID").innerHTML = room;

    socket.emit('join', {'room': room})
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

socket.on('found', async function (data) {
    console.log("found");
    // var prevcookie = document.cookie
    // console.log(prevcookie);
    // prevcookie = prevcookie + ";
    // console.log(prevcookie);
    document.cookie = "room=" + data['room'];
    console.log(document.cookie);
    window.location.replace("http://localhost:5001/");
    window.location.href = "http://localhost:5001/";
})