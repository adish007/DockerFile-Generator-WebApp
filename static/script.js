document.getElementById("repo-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent form submission

    const repoUrl = document.getElementById("repo-url").value.trim();
    const resultDiv = document.getElementById("result");

    if (!repoUrl) {
        resultDiv.innerHTML = `<h2>Error:</h2><p>Please enter a valid GitHub repository URL.</p>`;
        return;
    }

    resultDiv.innerHTML = "Generating Dockerfile...";

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `repo_url=${encodeURIComponent(repoUrl)}`,
        });

        const data = await response.json();
        if (response.ok) {
            if (data.dockerfile) {
                const escapedDockerfile = data.dockerfile
                    .replace(/&/g, "&amp;")
                    .replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;");
                resultDiv.innerHTML = `<h2>Generated Dockerfile:</h2><pre>${escapedDockerfile}</pre>`;
            } else {
                resultDiv.innerHTML = `<h2>Error:</h2><p>No Dockerfile content received.</p>`;
            }
        } else {
            resultDiv.innerHTML = `<h2>Error:</h2><p>${data.error}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<h2>Error:</h2><p>${error.message}</p>`;
    }
});
