let addFiveMinutesButton = document.getElementById('addFiveMinutes');
let subFiveMinutesButton = document.getElementById('subFiveMinutes');
let minutesOfBreak = document.getElementById('minutesOfBreak');


function calcMinutes(inputElement, minutes, option){
    let value = Number(inputElement.value);
    if (isNaN(value)) value = 0;

    if (option === "add"){
        value += minutes
    }
    else if (option === "sub" && value > 0){
        value -= minutes
    }
    inputElement.value = value;
}


addFiveMinutesButton.addEventListener("click", function (){
    calcMinutes(minutesOfBreak, 5, "add");
});

subFiveMinutesButton.addEventListener("click", function(){
    calcMinutes(minutesOfBreak, 5, "sub");
});