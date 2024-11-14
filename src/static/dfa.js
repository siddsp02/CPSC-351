const stateInput = document.getElementById("state-input");
let states = Number(stateInput.value);

const symbolInput = document.getElementById("symbol-input");
let symbols = Number(symbolInput.value);

stateInput.addEventListener("input", (e) => {
    states = Number(e.target.value);
    createTable(states, symbols);
});

symbolInput.addEventListener("input", (e) => {
    symbols = Number(e.target.value);
    createTable(states, symbols);
});

const createTable = (states, symbols) => {
    const table = document.getElementById("table");
    table.innerHTML = "";       // Clear existing table content.
    const startCharCode = 97;   // ASCII code for 'a'.
    for (let i = 0; i <= states; ++i) {
        const tr = document.createElement("tr");
        for (let j = 0; j <= symbols; ++j) {
            const td = document.createElement("td");
            if (i === 0 && j === 0)
                td.textContent = "";
            else if (i === 0 && j > 0)
                td.textContent = String.fromCharCode(startCharCode + j - 1);
            else if (j === 0 && i > 0)
                td.textContent = `q${i - 1}`;
            else
                td.innerHTML = `<input type="text"/>`;
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
}

const arrayToTransitionTable = (arr) => {
    const asciiLowerCaseLetters = "abcdefghijklmnopqrstuvwxyz";
    const transitionTable = {};
    for (let i = 0; i < arr.length; ++i) {
        const state = `q${i}`;
        transitionTable[state] = {};
        for (let j = 0; j < arr[i].length; ++j) {
            const symbol = asciiLowerCaseLetters[j];
            transitionTable[state][symbol] = arr[i][j];
        }
    }
    return transitionTable;
}

const submitForm = async (event) => {
    console.log(event);
    event.preventDefault();
    const arr = getTableValues();
    const transitionTable = arrayToTransitionTable(arr);
    try {
        const response = await fetch("/submit", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(transitionTable)
        });
        if (response.ok) {
            const result = await response.json();
            console.log("Response:", result);
        } else {
            console.error("Error submitting form:", response.statusText);
        }
    } catch (error) {
        console.error(error);
    }
};

const getTableValues = () => {
    const table = document.getElementById("table");
    const rows = table.getElementsByTagName("tr");
    const values = [];
    for (let i = 1; i < rows.length; ++i) {
        const row = [];
        const cells = rows[i].getElementsByTagName("td");
        for (let j = 0; j < cells.length; ++j) {
            const input = cells[j].querySelector("input");
            if (input) {
                row.push(input.value);
            }
        }
        values.push(row);
    }
    return values;
}
