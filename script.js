function analyzeText() {
    let userInput = document.getElementById("userInput").value.trim();
    if (!userInput) {
        alert("Please enter a message!");
        return;
    }

    fetch('http://127.0.0.1:5000/predict', {  // Correct API URL
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: userInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        let outputDiv = document.getElementById("output");

        if (data.error) {
            outputDiv.innerHTML = `<span style="color: red;">Error: ${data.error}</span>`;
        } else {
            outputDiv.innerHTML = `Prediction: ${data.prediction} <br> Confidence: ${data.confidence}%`;
            outputDiv.className = "output-box " + (data.prediction === "Offensive" ? "warning" : "success");

            let historyDiv = document.getElementById("history");
            let entry = document.createElement("div");
            entry.innerHTML = `<b>${userInput}</b> - ${data.prediction} (${data.confidence}%)`;
            historyDiv.prepend(entry);
        }
    })
    .catch(error => console.error("Fetch Error:", error));
}
