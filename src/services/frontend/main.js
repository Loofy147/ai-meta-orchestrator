/* eslint-env browser */
fetch("/api/")
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").innerText = data.message;
    });
