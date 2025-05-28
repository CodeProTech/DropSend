// Get references to HTML elements
const input = document.getElementById("codeInput");
const button = document.getElementById("checkCodeBtn");
const errorMessage = document.getElementById("errorMessage");
const downloadLink = document.getElementById("downloadLink");

// Only allow numbers and enable button if 6 digits are typed
input.addEventListener("input", () => {
  input.value = input.value.replace(/[^0-9]/g, ""); // remove non-numbers
  button.disabled = input.value.length !== 6; // only enable if length is 6
});

// When the button is clicked
button.addEventListener("click", () => {
  const enteredCode = input.value.trim(); // get the input and remove spaces

  fetch("/check_code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: enteredCode }), // send the code to server
  })
    .then(async (response) => {
      const data = await response.json(); // parse response
      if (!response.ok) throw new Error(data.error || "Unknown error");
      return data;
    })
    .then((data) => {
      if (data.success) {
        errorMessage.textContent = ""; // clear error message

        // Create a list for download links
        const ul = document.createElement("ul");
        data.files.forEach(file => {
          const li = document.createElement("li");
          const a = document.createElement("a");
          a.href = `/download/${data.folder}/${file}`; // link to file
          a.textContent = file;
          a.setAttribute("download", file); // trigger download
          li.appendChild(a);
          ul.appendChild(li);
        });

        // Clear old content and add the new list
        downloadLink.innerHTML = "";
        downloadLink.appendChild(ul);
        downloadLink.style.display = "block"; // make it visible

      } else {
        downloadLink.style.display = "none";
        errorMessage.textContent = data.error || "Invalid code.";
      }
    })
    .catch((err) => {
      downloadLink.style.display = "none";
      errorMessage.textContent = err.message || "Server error! Try again later.";
    });
});

// Allow pressing Enter to trigger the check
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter" && !button.disabled) {
    button.click();
  }
});
