const input = document.getElementById("codeInput");
const button = document.getElementById("checkCodeBtn");
const errorMessage = document.getElementById("errorMessage");
const downloadLink = document.getElementById("downloadLink");

// Nur Zahlen erlauben und Button nur aktivieren, wenn 6 Zeichen eingegeben sind
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
    if (!response.ok) throw new Error(data.error || "Unbekannter Fehler");
    return data;
  })
  .then((data) => {
    if (data.success) {
      errorMessage.textContent = "";

      // Liste dynamisch erstellen
      const ul = document.createElement("ul");
      data.files.forEach(file => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = `/download/${data.folder}/${file}`;
        a.textContent = file;
        a.setAttribute("download", file);
        li.appendChild(a);
        ul.appendChild(li);
      });

      // Bisherige Inhalte löschen & neue hinzufügen
      downloadLink.innerHTML = "";
      downloadLink.appendChild(ul);
      downloadLink.style.display = "block";

    } else {
      downloadLink.style.display = "none";
      errorMessage.textContent = data.error || "Ungültiger Code.";
    }
  })
  .catch((err) => {
    downloadLink.style.display = "none";
    errorMessage.textContent = err.message || "Serverfehler! Bitte später erneut versuchen.";
  });
});

input.addEventListener("keypress", (e) => {
if (e.key === "Enter" && !button.disabled) {
  button.click();
}
});
