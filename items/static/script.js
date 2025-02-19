document.addEventListener("DOMContentLoaded", function() {

    // Submit Lost Item
    const lostForm = document.getElementById("lostForm");
    if (lostForm) {
        lostForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const formData = new FormData();
            formData.append("name", document.getElementById("name").value);
            formData.append("description", document.getElementById("description").value);
            formData.append("location", document.getElementById("location").value);
            formData.append("image", document.getElementById("image").files[0]);

            fetch("/api/submit_lost/", { method: "POST", body: formData })
                .then(response => response.json())
                .then(data => document.getElementById("responseMessage").innerText = data.message)
                .catch(error => console.error("Error:", error));
        });
    }

    // Submit Found Item
    const foundForm = document.getElementById("foundForm");
    if (foundForm) {
        foundForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const formData = new FormData();
            formData.append("location", document.getElementById("location").value);
            formData.append("image", document.getElementById("image").files[0]);

            fetch("/api/submit_found/", { method: "POST", body: formData })
                .then(response => response.json())
                .then(data => document.getElementById("responseMessage").innerText = data.message)
                .catch(error => console.error("Error:", error));
        });
    }

    // Match Lost & Found Items
    const matchForm = document.getElementById("matchForm");
    if (matchForm) {
        matchForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const lostItemId = document.getElementById("lostItemId").value;

            fetch("/api/match_items/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "lost_item_id": lostItemId })
            })
            .then(response => response.json())
            .then(data => {
                let resultsHTML = "<h3>Matching Found Items:</h3>";
                data.matches.forEach(match => {
                    resultsHTML += `<p>Found Item ID: ${match.found_item_id}, Similarity Score: ${match.score.toFixed(2)}, Distance: ${match.distance_km.toFixed(2)} km</p>`;
                });
                document.getElementById("matchResults").innerHTML = resultsHTML;
            })
            .catch(error => console.error("Error:", error));
        });
    }

});
