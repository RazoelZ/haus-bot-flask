const api = "http://localhost:3000";


// Get the elements for Modal 1
var modal = document.getElementById("modal");
var btn = document.getElementById("chat-group-btn");
var span = document.getElementsByClassName("close")[0];

// Event listener to open Modal 1
btn.onclick = function () {
    modal.style.display = "block";
};

// Event listener to close Modal 1
span.onclick = function () {
    modal.style.display = "none";
};

// Close Modal 1 when clicking outside of it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

// Handle form submission for Modal 1
document.getElementById("chat-form").onsubmit = function (event) {
    event.preventDefault(); // Prevent default form submission

    var message = document.getElementById("message").value;

    fetch(`${api}/sendMessageTolark`
        , {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
            modal.style.display = "none"; // Close Modal 1 after sending the message
            alert("Message sent successfully!");
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Error sending message.");
        });
};

// Get the elements for Modal 2
var modal2 = document.getElementById("modal2");
var btn2 = document.getElementById("chat-btn");
var span2 = document.getElementsByClassName("close")[1];
var userSelect = document.getElementById("user-select");
var messageInput = document.getElementById("message2");

// Event listener to open Modal 2 and populate user options
btn2.onclick = function () {
    fetch(`${api}/getUserFromDepartment`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer t-g20572da3VEMR6K5EHMPL3UR2M4QHPFPNOEOSNTY"
        },
        body: JSON.stringify({ department_id: "od-b9d1cc50992f360f1c25f89527274b97" }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
            // Populate select options with response data
            userSelect.innerHTML = ""; // Clear previous options
            data.forEach((user) => {
                var option = document.createElement("option");
                option.value = user.user_id;
                option.textContent = user.name;
                userSelect.appendChild(option);
            });

            modal2.style.display = "block"; // Show Modal 2 after fetching data
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Error fetching user data.");
        });
};

// Event listener to close Modal 2
span2.onclick = function () {
    modal2.style.display = "none";
};

// Close Modal 2 when clicking outside of it
window.onclick = function (event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
};

// Handle form submission for Modal 2
document.getElementById("chat-form2").onsubmit = function (event) {
    event.preventDefault(); // Prevent default form submission

    var message = messageInput.value;
    var selectedUserId = userSelect.value;

    fetch(`${api}/sendMessageTolarkChat`
        , {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: message,
                receive_id: selectedUserId
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
            modal2.style.display = "none"; // Close Modal 2 after sending the message
            alert("Message sent successfully!");
        })
        .catch((error) => {
            console.error("Error:", selectedUserId);
            console.error("Error:", error);
            console.error("Error:", error);
            console.error("Error:", message);
            alert("Error sending message.");
        });
};