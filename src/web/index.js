console.log("hi");

const stateInput = document.getElementById("state-input");
let states = Number(stateInput.value);

const symbolInput = document.getElementById("symbol-input");
let symbols = Number(symbolInput.value);

stateInput.addEventListener("input", (e) => {
  states = Number(e.target.value);
  createTable(states, symbols);
});

symbolInput.addEventListener("input", (e) => {
  symbols = Number(symbolInput.value);
  symbols = Number(e.target.value);
  createTable(states, symbols);
});

const createTable = (states, symbols) => {
  const table = document.getElementById("table");
  table.innerHTML = ""; // Clear any existing table content

  // ASCII code for 'a'
  const startCharCode = 97;

  for (let i = 0; i < states + 1; i++) {
    const tr = document.createElement("tr");

    for (let j = 0; j < symbols + 1; j++) {
      const td = document.createElement("td");

      if (i === 0 && j === 0) {
        td.textContent = "";
      } else {
        // Set headers for the first row
        if (i === 0 && j > 0) {
          td.textContent = String.fromCharCode(startCharCode + j - 1);
        }
        // Set headers for the first column
        else if (j === 0 && i > 0) {
          td.textContent = `q${i - 1}`;
        }
        // Create input cells for the rest
        else {
          td.innerHTML = `<input type="text" />`;
        }
      }

      tr.appendChild(td);
    }

    table.appendChild(tr);
  }
};

const submitForm = async (event) => {
  console.log(event);

  event.preventDefault(); // Prevents the form from submitting the traditional way

  const arr = getTableValues();
  console.log("🚀 ~ submitForm ~ arr:", arr);
  // Send data as a POST request
  //   try {
  //       const response = await fetch('/submit', {
  //           method: 'POST',
  //           headers: {
  //               'Content-Type': 'application/json'
  //           },
  //           body: JSON.stringify({ states, symbols })
  //       });

  //       if (response.ok) {
  //           const result = await response.json();
  //           console.log('Response:', result);
  //       } else {
  //           console.error('Error submitting form:', response.statusText);
  //       }
  //   } catch (error) {
  //       console.error('Fetch error:', error);
  //   }
};

const getTableValues = () => {
  const table = document.getElementById("table");
  const rows = table.getElementsByTagName("tr");
  const values = [];

  for (let i = 1; i < rows.length; i++) {
    const row = [];
    const cells = rows[i].getElementsByTagName("td");
    for (let j = 0; j < cells.length; j++) {
      const input = cells[j].querySelector("input");
      if (input) {
        row.push(input.value); // Get the value from each input
      }
    }
    values.push(row); // Add the row array to the values array
  }

  return values;
};
