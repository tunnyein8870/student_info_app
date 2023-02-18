let addBtnContainer = document.createElement('div')
addBtnContainer.className = "add-btn-container"
let addBtnLabel = document.createElement('label')
addBtnLabel.innerHTML = "Additional Information"
addBtnLabel.className = "add-btn-label"
let addBtn = document.createElement('input')
addBtn.name = 'add-btn'
addBtn.type = 'button'
addBtn.value = "Add"
addBtn.className = "add-btn"
let btnDyFormDiv = document.getElementById('btn-dy-form')
addBtnContainer.append(addBtnLabel, addBtn)
btnDyFormDiv.append(addBtnContainer)

let countInputContainer = 0;
let dyForm = document.getElementById('dy-form')
dyForm.className = "dy-form"

document.body.onload = ()=>{
    if (Object.keys(jsonData).length > 0){
        displayData(jsonData)
        console.log(Object.keys(jsonData.length))
    }
    else{
        console.log("do nothing")
    }
}

addBtn.addEventListener("click", () => {
    createInputDiv()
})


function createInputDiv() {
    let inputContainer = document.createElement('div')
    let delBtn = document.createElement('button')
    delBtn.innerText = "✖"
    delBtn.className = 'del-btn'
    delBtn.name = 'del-btn'
    for (i = 0; i < 5; i++) {
        let form_input = document.createElement('input')
        form_input.type = "text"
        // var variable = (condition) ? (true block) : ((condition2) ? (true block2) : (else block2))
        // let check_subject = (i==1) ? ("maths") : ((i==2) ? ("arts") : ("physics"))
        let check_subject = 
        (i==0) ? ("subjectId") : 
        (i==1) ? ("maths") : 
            (
            (i==2) ? ("arts") : 
                (
                    (i==3) ? ("physics") : ("year")
                )
            )
        form_input.className = check_subject
        form_input.placeholder = `${check_subject.toUpperCase()}`
        if (check_subject == 'subjectId'){
            form_input.setAttribute('hidden', true)
            // form_input.setAttribute('disabled', true)
            form_input.name = check_subject + "_" + countInputContainer   // to be able to call request by flask
            form_input.value = check_subject + "_" + "NoVal" + countInputContainer  
        }
        else{
            form_input.name =  check_subject + "_" + "Val" + countInputContainer
        }
        inputContainer.append(form_input, delBtn)
    }
    dyForm.append(inputContainer)
    countInputContainer++;
    delBtn.addEventListener("click", () => {
        dyForm.removeChild(inputContainer)
        countInputContainer--;
    })
}

function displayData(data) {
    let ids = data.map(row => row[0]);              // get id list from json_data from flask backend
    for (let i = 0; i < data.length; i++) {         // loop to get each id in ids
        console.log(ids[i])
        let inputContainer = document.createElement('div');
        let delBtn = document.createElement('button');
        delBtn.innerText = "✖";
        delBtn.className = 'del-btn';
        delBtn.name = 'del-btn' + ids[i];
        delBtn.value = ids[i]
        for (let j = 0; j < data[i].length; j++) {
            let form_input = document.createElement('input');
            form_input.type = "text";
            let check_subject = (j == 0) ? "subjectId" :
                                (j === 1) ? "maths" :
                                 (j === 2) ? "arts" :
                                 (j === 3) ? "physics" : 
                                 "year";
            form_input.className = check_subject;
            if (check_subject == "subjectId"){
                form_input.setAttribute('hidden', true)
                // form_input.setAttribute('disabled', true)
                form_input.name = check_subject + "_" + ids[i] + countInputContainer
                form_input.value = ids[i]
            }
            else{
                form_input.placeholder = `${check_subject.toUpperCase()}`;
                form_input.name = check_subject + "_" + data[i][j] + countInputContainer;
                form_input.value = data[i][j]
            }
            inputContainer.append(form_input, delBtn);
        }
        dyForm.append(inputContainer);
        countInputContainer++;
        delBtn.addEventListener("click", () => {
            /* When user wants to delete each record immediately, use this form.
            it works with python flask, check in server.py */
            // let form  = document.createElement("form");
            // form.method = "POST";
            // form.action = '/delete';
            // let idInput = document.createElement('input');
            // idInput.type = 'hidden';
            // idInput.name = 'subject_id'
            // idInput.value = delBtn.value;
            // form.append(idInput);
            // document.body.append(form)
            // form.submit();
            dyForm.removeChild(inputContainer);
            countInputContainer--;
        });
    }
}



