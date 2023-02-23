let inputBoxes = document.querySelectorAll('.input-box input')
let button = document.querySelector('.button input[type="submit"]');
let btnText = button.value.trim();
let emptyInput = ()=>{
    for (let i = 0; i < inputBoxes.length; i++){
        if(inputBoxes[i].value == ''){
            return false
        }
    }
}
button.addEventListener('click', ()=>{
    if (btnText == 'Create'){
        if (emptyInput() == false){
            alert("Please Enter Rquired Fields.")
        }
        else{
            alert("Student Created.")
        }
    }
    else{
        alert("Student Updated.")
    }
})
