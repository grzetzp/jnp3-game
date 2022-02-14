var socket = io()
var logAttack = document.getElementById('log_attack')
var logEcho = document.getElementById('log_echo')
var attackForm = document.getElementById('attack')
var trainForm = document.getElementById('train')
var leaveForm = document.getElementById('leave')
var emitData = new FormData(attackForm)
var emitForm = document.getElementById('emit')
var joinForm = document.getElementById('join_game')
var timeout = document.getElementById('timeout')
var my_success = document.getElementById('my_success')
var op_success = document.getElementById('op_success')
var my_attck_nr = 0
var op_attck_nr = 0
var my_name = getCookie("username")
var my_attck_scs = 0.5
var op_attck_scs = 0.5

var ranking_counted = false

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = 0;
        }

        if (timer === 0 && ranking_counted === false) {
            ranking_counted = true
            attackForm.style.display = 'none';
            trainForm.style.display = 'none';
            if (my_attck_nr > op_attck_nr) {
                timeout.textContent = "YOU WON! YOU WON! YOU WON! YOU WON! YOU WON! YOU WON! YOU WON! YOU WON! YOU WON!"
                socket.emit('win')
            } else if (my_attck_nr < op_attck_nr) {
                timeout.textContent = "YOU LOST! YOU LOST! YOU LOST! YOU LOST! YOU LOST! YOU LOST! YOU LOST! YOU LOST! YOU LOST!"
                socket.emit('lose')
            } else {
                timeout.textContent = "IT'S A TIE! IT'S A TIE! IT'S A TIE! IT'S A TIE! IT'S A TIE! IT'S A TIE! IT'S A TIE! IT'S A TIE! IT'S A TIE!"
                socket.emit('tie')
            }
        }
    }, 1000);
}

window.onload = function () {
    var fiveMinutes = 20,
        display = document.querySelector('#time');
    startTimer(fiveMinutes, display);
};

attackForm.addEventListener('submit', attackAction)
trainForm.addEventListener('submit', trainAction)

function getCookie(cName) {
  const name = cName + "=";
  const cDecoded = decodeURIComponent(document.cookie); //to be careful
  const cArr = cDecoded.split('; ');
  let res;
  cArr.forEach(val => {
    if (val.indexOf(name) === 0) res = val.substring(name.length);
  })
  return res
}

function attackAction(event) {
    event.preventDefault();
    console.log("Attack")
    socket.emit('attack')

    return false
}

function trainAction(event) {
    event.preventDefault();
    console.log("Train")
    socket.emit('train')

    return false
}

emitForm.addEventListener('submit', emitAction)

function emitAction(event) {
    event.preventDefault();
    console.log("Submit " + emitForm['emit_data'].value)
    socket.emit('my_event', {data: emitForm['emit_data'].value})
}

(function(){
    console.log("joining game");
    socket.emit('join_game');
})();

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


socket.on('train_response', function (msg, callback) {
    if (msg['player'] === my_name)
        my_attck_scs = msg.data
    else
        op_attck_scs = msg.data

    my_success.textContent = my_attck_scs
    op_success.textContent = op_attck_scs

    if (callback) {
        callback()
    }
})


socket.on('attack_response', function (msg, callback) {
    var br = document.createElement("br");
    logAttack.appendChild(br);
    console.log(typeof(msg.data))
    logAttack.innerHTML += '\r\n'

    if (msg['player'] === my_name)
        my_attck_nr += msg.data
    else
        op_attck_nr += msg.data


    logAttack.textContent = "MY ATTACKS " + my_attck_nr + " OPPONENT ATTACKS " + op_attck_nr


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