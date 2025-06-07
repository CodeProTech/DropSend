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
          const a = document.createElement("a");
          a.href = `/download/${data.folder}/${file}`;
          a.textContent = file;
          a.setAttribute("download", file);
          a.classList.add("btn", "btn-primary");

          container.appendChild(a);
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
