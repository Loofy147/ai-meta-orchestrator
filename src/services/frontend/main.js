fetch("http://localhost:5000/")
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").innerText = data.message;
    });
