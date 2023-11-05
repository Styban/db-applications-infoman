// Function to fetch and populate data
function fetchDataAndPopulateTable() {
// Get a reference to the table body
const tableBody = document.querySelector("#data-table tbody");

// Clear the existing table content
tableBody.innerHTML = "";

// Fetch JSON data from the remote URL
fetch("http://127.0.0.1:8000/api/student")
    .then((response) => response.json())
    .then((jsonData) => {
    // Populate the table with JSON data
    jsonData.forEach((data) => {
        const row = document.createElement("tr");

        //create a td for my ID
        const tdid = document.createElement("td");
        tdid.textContent = data.student_id;

        const tdFname = document.createElement("td");
        tdFname.textContent = data.first_name;

        const tdMname = document.createElement("td");
        tdMname.textContent = data.middle_name;

        const tdLname = document.createElement("td");
        tdLname.textContent = data.last_name;

        const tdDOB = document.createElement("td");
        tdDOB.textContent = data.dob;

        const tdGender = document.createElement("td");
        tdGender.textContent = data.gender;

        const tdCivilStatus = document.createElement("td");
        tdCivilStatus.textContent = data.civil_status;

        const tdPhone = document.createElement("td");
        tdPhone.textContent = data.phone;

        const tdEmail = document.createElement("td");
        tdEmail.textContent = data.email;

        const tdAction = document.createElement("td");
        const deleteButton = document.createElement("button");
        deleteButton.className = "btn btn-danger btn-sm"
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", () => {
        confirmDelete(data.student_id);
        });

        const updateButton = document.createElement("button");
        updateButton.className = "btn btn-warning btn-sm"
        updateButton.textContent = "Update";

        updateButton.addEventListener("click", () => {
            editStudent(data.student_id);
        });

        tdAction.appendChild(deleteButton);
        tdAction.appendChild(updateButton);

        row.appendChild(tdid);
        row.appendChild(tdFname);
        row.appendChild(tdMname);
        row.appendChild(tdLname);
        row.appendChild(tdDOB);
        row.appendChild(tdGender);
        row.appendChild(tdCivilStatus);
        row.appendChild(tdPhone);
        row.appendChild(tdEmail);
        row.appendChild(tdAction);

        tableBody.appendChild(row);
    });
    })
    .catch((error) => {
    console.error("Error fetching data:", error);
    });
}



// Function to search and filter the table
function searchTable(event) {
event.preventDefault();
const searchTerm = document.getElementById("search-input").value;

// Get a reference to the table body
const tableBody = document.querySelector("#data-table tbody");

// Clear the existing table content
tableBody.innerHTML = "";

// Fetch data from the '/api/search' endpoint with the search term
fetch(`http://127.0.0.1:8000/api/student?q=${searchTerm}`)
    .then((response) => response.json())
    .then((jsonData) => {
    // Populate the table with JSON data
    jsonData.forEach((data) => {
        const row = document.createElement("tr");

        //create a td for my ID
        const tdid = document.createElement("td");
        tdid.textContent = data.student_id;

        const tdFname = document.createElement("td");
        tdFname.textContent = data.first_name;

        const tdMname = document.createElement("td");
        tdMname.textContent = data.middle_name;

        const tdLname = document.createElement("td");
        tdLname.textContent = data.last_name;

        const tdDOB = document.createElement("td");
        tdDOB.textContent = data.dob;

        const tdGender = document.createElement("td");
        tdGender.textContent = data.gender;

        const tdCivilStatus = document.createElement("td");
        tdCivilStatus.textContent = data.civil_status;

        const tdPhone = document.createElement("td");
        tdPhone.textContent = data.phone;

        const tdEmail = document.createElement("td");
        tdEmail.textContent = data.email;

        const tdAction = document.createElement("td");
        const deleteButton = document.createElement("button");

        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", () => {
        confirmDelete(data.student_id);
        });
        tdAction.appendChild(deleteButton);

        row.appendChild(tdid);
        row.appendChild(tdFname);
        row.appendChild(tdMname);
        row.appendChild(tdLname);
        row.appendChild(tdDOB);
        row.appendChild(tdGender);
        row.appendChild(tdCivilStatus);
        row.appendChild(tdPhone);
        row.appendChild(tdEmail);
        row.appendChild(tdAction);

        tableBody.appendChild(row);
    });
    })
    .catch((error) => {
    console.error("Error fetching data:", error);
    });
}



function deleteStudent(id) {
// Send an HTTP DELETE request to the server
fetch(`http://127.0.0.1:8000/api/student/${id}`, {
    method: "DELETE",
})
    .then((response) => response.json())
    .then((data) => {
    // If the deletion was successful, refresh the table data
    fetchDataAndPopulateTable();
    })
    .catch((error) => {
    console.error("Error deleting student:", error);
    });
}

// Function to call deleteStudent with a specific student ID
function confirmDelete(id) {
if (confirm("Are you sure you want to delete this student?")) {
    deleteStudent(id);
}
}

function editStudent(id) {
    fetch(`http://127.0.0.1:8000/api/update/${id}`, {
    method :'GET',
    })
    .then((response) => response.json())
    .then((data) => {
    // If the deletion was successful, refresh the table data
    
    })
    .catch((error) => {
    console.error("Error deleting student:", error);
    });
}

// Add an event listener to fetch data after the page is loaded
window.addEventListener("DOMContentLoaded", fetchDataAndPopulateTable);