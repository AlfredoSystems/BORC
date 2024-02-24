document.addEventListener('DOMContentLoaded', function () {
    const startButton = document.querySelector('.start');
    const stopButton = document.querySelector('.stop');
    const replayButton = document.querySelector('.replay');
    const timerBar = document.querySelector('.timer-bar');
    const redTrapInput = document.querySelector('.alliance.red .objective > span:first-child + input[type="number"]');
    const blueTrapInput = document.querySelector('.alliance.blue .objective > span:first-child + input[type="number"]');
    const redAmpInput = document.querySelector('.alliance.red input[name="amp"]');
    const blueAmpInput = document.querySelector('.alliance.blue input[name="amp"]');
    const redTotalPointsInput = document.querySelector('.alliance.red .total-points input');
    const blueTotalPointsInput = document.querySelector('.alliance.blue .total-points input');

    const audioAuto = document.getElementById('audioAuto');
    const audioTeleop = document.getElementById('audioTeleop');
    const audioEndgame = document.getElementById('audioEndgame');
    const audioEnd = document.getElementById('audioEnd');
    const audioFault = document.getElementById('audioFault');

    let timerInterval;
    let timeLeft = 150; // Total time in seconds
    let isRunning = false;

    startButton.addEventListener('click', startTimer);
    stopButton.addEventListener('click', stopTimer);
    replayButton.addEventListener('click', replayTimer);

    document.addEventListener('keydown', function (event) {
        if (event.key === 'w' || event.key === 'W') {
            increaseScore(redTrapInput);
            console.log('w')
        } else if (event.key === 'e' || event.key === 'E') {
            increaseScore(blueTrapInput);
        } else if (event.key === 's' || event.key === 'S') {
            increaseScore(redAmpInput);
        } else if (event.key === 'd' || event.key === 'D') {
            increaseScore(blueAmpInput);
        }
    });

    function startTimer() {
        if (!isRunning) {
            isRunning = true;
            timerInterval = setInterval(updateTimer, 1000);
            playSound(audioAuto);
        }
    }

    function stopTimer() {
        clearInterval(timerInterval);
        isRunning = false;
        playSound(audioFault);
    }

    function replayTimer() {
        stopTimer();
        timerBar.style.backgroundColor = '#4CAF50'; // Reset timer bar color
        timeLeft = 150; // Reset time
        updateTimerDisplay();
    }

    function updateTimer() {
        timeLeft--;
        updateTimerDisplay();

        // Change timer bar color as it progresses
        //let percentageLeft = (timeLeft / 150) * 100;
        //if (percentageLeft < 30) {
        //    timerBar.style.backgroundColor = '#ccc'; // Change to grey when less than 30% left
        //}

        if (timeLeft <= 0) {
            stopTimer();
            // Additional logic when timer reaches zero (e.g., game over)
        }
    }

    function updateTimerDisplay() {
        let percentageLeft = (timeLeft / 150) * 100;
     //timerBar.style.width = timeLeft + '%';
        timerBar.style.background = `linear-gradient(to right, green ${percentageLeft}%, grey 0%)`;

    }

    function increaseScore(inputElement) {
        let currentValue = parseInt(inputElement.value);
        inputElement.value = currentValue + 1;
        updateTotalPoints();
    }

    function updateTotalPoints() {
        let redTotal = parseInt(redTrapInput.value) + parseInt(redAmpInput.value);
        let blueTotal = parseInt(blueTrapInput.value) + parseInt(blueAmpInput.value);

        redTotalPointsInput.value = redTotal;
        blueTotalPointsInput.value = blueTotal;
    }



});

function playSound(audioElement){
    audioElement.pause();
    audioElement.currentTime = 0;
    audioElement.play();
}