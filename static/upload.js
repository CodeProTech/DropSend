const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');
const progressBar = document.getElementById('progress-bar');
const liste = document.getElementById("file-list");

dropArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropArea.style.backgroundColor = '#005566';
});

dropArea.addEventListener('dragleave', () => {
  dropArea.style.backgroundColor = '';
});

dropArea.addEventListener('drop', (e) => {
  e.preventDefault();
  dropArea.style.backgroundColor = '';
  handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', () => {
  handleFiles(fileInput.files);
});

function handleFiles(files) {
  Array.from(files).forEach((file) => {
    const li = document.createElement('li');
    li.classList.add('file-item');
    li.innerHTML = `
      ${file.name}
      <button onclick="removeFile(this, '${file.name}')">Löschen</button>
    `;
    fileList.appendChild(li);

    const progressContainer = document.createElement('div');
    progressContainer.classList.add('progress-bar-container');
    const progress = document.createElement('div');
    progress.classList.add('progress-bar');
    progressContainer.appendChild(progress);
    li.appendChild(progressContainer);

    uploadFile(file, progress);
  });
}

function uploadFile(file, progressElement) {
  const formData = new FormData();
  formData.append('file', file);

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/upload', true);

  xhr.upload.onprogress = function(e) {
    if (e.lengthComputable) {
      const percent = (e.loaded / e.total) * 100;
      progressElement.style.width = percent + '%';
    }
  };

  xhr.onload = function() {
    if (xhr.status == 200) {
      console.log('Upload abgeschlossen');
    } else {
      console.log('Fehler beim Hochladen');
    }
  };

  xhr.send(formData);
}

function removeFile(button, filename) {
  const fileItem = button.closest('.file-item');
  fileItem.remove();

  fetch("/delete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ filename: filename })
  })
    .then(response => response.json())
    .then(data => {
      console.log("Datei gelöscht:", data.message);
    })
    .catch(error => {
      console.error("Fehler beim Löschen:", error);
    });
}
