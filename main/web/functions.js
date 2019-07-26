eel.expose(getValues);
function getValues() {
    var values = [];
    var inputs = document.getElementsByTagName("input");

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].getAttribute("type") == "text"){
        values.push(inputs[i].value);
        }
    }
    finalValues = fixArray(values);
    return finalValues;
}

eel.expose(defineSudoku);
function defineSudoku(arr) {
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].value    = arr[i];
        if (arr[i] != "") {
            inputs[i].disabled = true;
        }
    }
}


async function restartGame() {
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].value = "";
        inputs[i].style.color = "black";
        inputs[i].disabled = false;
    }
    var sudokuBoard = await eel.generate_sudoku()()
    defineSudoku(sudokuBoard);
}

function fixArray(arr) {
    var finalArr = [];
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] == "") {
            finalArr[i] = 0;
        } else {
            finalArr[i] = parseInt(arr[i]);
        }
    }
    return finalArr;
}

async function getButtonClick() {
    let solutionArray = await eel.sudoku_solver(getValues())()
    var inputs = document.getElementsByTagName("input");

    for (var i = 0; i < solutionArray.length; i++) {
        if (inputs[i].value != solutionArray[i]) {
            inputs[i].value = solutionArray[i];
            inputs[i].style.color = "red";
        }
        inputs[i].disabled = true;
    }
}
