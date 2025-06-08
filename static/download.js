const input = document.getElementById("codeInput");
const button = document.getElementById("checkCodeBtn");
const errorMessage = document.getElementById("errorMessage");
const downloadLink = document.getElementById("downloadLink");

input.addEventListener("input", () => {
  input.value = input.value.replace(/[^0-9]/g, "");
  button.disabled = input.value.length !== 6;
});

button.addEventListener("click", () => {
  const enteredCode = input.value.trim();

  fetch("/check_code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: enteredCode }),
  })
    .then(async (response) => {
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Unknown error");
      return data;
    })
    .then((data) => {
      if (data.success) {
        errorMessage.textContent = "";

        const container = document.createElement("div");
        container.style.display = "flex";
        container.style.flexWrap = "wrap";
        container.style.gap = "10px";
        container.style.justifyContent = "center";

        data.files.forEach(file => {
          const downloadButton = document.createElement("button");
          downloadButton.textContent = file;
          downloadButton.classList.add("btn", "btn-primary");
          downloadButton.onclick = () => {
            // Erstelle einen versteckten Link und klicke ihn programmatisch
            const link = document.createElement('a');
            link.href = `/download/${data.folder}/${file}`;
            link.download = file; // Setzt den Download-Attributnamen
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          };

          container.appendChild(downloadButton);
        });

        downloadLink.innerHTML = "";
        downloadLink.appendChild(container);
        downloadLink.style.display = "block";
      } else {
        downloadLink.style.display = "none";
        errorMessage.textContent = data.error || "Invalid code.";
      }
    })
    .catch((err) => {
      downloadLink.style.display = "none";
      errorMessage.textContent = err.message || "Server error. Please try again later.";
    });
});

input.addEventListener("keypress", (e) => {
  if (e.key === "Enter" && !button.disabled) {
    button.click();
  }
});