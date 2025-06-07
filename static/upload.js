// Get elements from the page
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');
const progressBar = document.getElementById('progress-bar');
const liste = document.getElementById("file-list");

// When files are dragged over the drop area
dropArea.addEventListener('dragover', (e) => {
  e.preventDefault(); // prevent default to allow drop
  dropArea.style.backgroundColor = '#005566'; // change background color on hover
});

// When dragged files leave the drop area
dropArea.addEventListener('dragleave', () => {
  dropArea.style.backgroundColor = ''; // reset background color
});

// When files are dropped in the drop area
dropArea.addEventListener('drop', (e) => {
  e.preventDefault(); // prevent default browser behavior
  dropArea.style.backgroundColor = ''; // reset background color
  handleFiles(e.dataTransfer.files); // handle dropped files
});

// When files are selected via file input
fileInput.addEventListener('change', () => {
  handleFiles(fileInput.files); // handle selected files
});

// Process each file to show in the list and start upload
function handleFiles(files) {
  Array.from(files).forEach((file) => {
    const li = document.createElement('li');
    li.classList.add('file-item');
    li.innerHTML = `
      ${file.name}
      <button onclick="removeFile(this, '${file.name}')">Delete</button>
    `; // show filename and delete button
    fileList.appendChild(li); // add to list

    // Create progress bar element
    const progressContainer = document.createElement('div');
    progressContainer.classList.add('progress-bar-container');
    const progress = document.createElement('div');
    progress.classList.add('progress-bar');
    progressContainer.appendChild(progress);
    li.appendChild(progressContainer); // add progress bar to list item

    uploadFile(file, progress); // start uploading the file
  });
}

// Upload the file with progress update
function uploadFile(file, progressElement) {
  const formData = new FormData();
  formData.append('file', file); // add file to form data

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/upload', true); // open POST request to /upload

  // Update progress bar during upload
  xhr.upload.onprogress = function(e) {
    if (e.lengthComputable) {
      const percent = (e.loaded / e.total) * 100;
      progressElement.style.width = percent + '%'; // fill progress bar
    }
  };

  // On upload complete
  xhr.onload = function() {
    if (xhr.status == 200) {
      console.log('Upload abgeschlossen'); // success message
    } else {
      console.log('Fehler beim Hochladen'); // error message
    }
  };

  xhr.send(formData); // send the form data with the file
}

// Remove a file from the list and delete it on the server
function removeFile(button, filename) {
  const fileItem = button.closest('.file-item'); // get the list item
  fileItem.remove(); // remove from UI

  // Send delete request to server
  fetch("/delete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ filename: filename }) // send filename to delete
  })
    .then(response => response.json())
    .then(data => {
      console.log("Datei gelöscht:", data.message); // confirm deletion
    })
    .catch(error => {
      console.error("Fehler beim Löschen:", error); // show error if any
    });
}
