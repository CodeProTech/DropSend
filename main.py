import os
import random
import secrets
import shutil
import socket
import string
from pathlib import Path
import webbrowser

from flask import Flask, render_template, jsonify, request, abort, send_from_directory
from werkzeug.utils import secure_filename
import qrcode

# Function to generate a secure random string of given length for download URLs.
# Uses letters (uppercase and lowercase) and digits.
def generate_secure_code_download(length=10):
    chars = string.ascii_letters + string.digits
    # secrets.choice provides cryptographically strong randomness.
    return ''.join(secrets.choice(chars) for _ in range(length))

# Function to generate a secure random string of given length for upload URLs.
# It is basically the same as the download code generator.
def generate_secure_code_upload(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

# Function to delete all contents inside a specified folder (files and subfolders).
# Useful to clear the upload directory before starting the app.
def clear_folder_contents(folder_path):
    folder = Path(folder_path)
    if folder.exists() and folder.is_dir():
        for item in folder.iterdir():
            try:
                if item.is_dir():
                    # Recursively delete subdirectories
                    shutil.rmtree(item)
                else:
                    # Delete files and symlinks
                    item.unlink()
            except Exception as e:
                # Ignore exceptions during deletion to avoid crashing
                pass

# Generate unique secure URLs for download and upload functionality.
ungurl = generate_secure_code_download(10)
ungurl_upload = generate_secure_code_upload(10)

# Get the local IP address of the machine (used for hosting the Flask server).
ip = socket.gethostbyname(socket.gethostname())

# Generate a random 6-digit numeric code as a string, padded with zeros if needed.
code =  f"{random.randint(0, 999999):06d}"

# Compose full HTTP URLs for download and upload endpoints, using the IP and port 5000.
link_download = f"http://{ip}:5000/download/{ungurl_upload}"
link_upload = f"http://{ip}:5000/{ungurl}"
link_another_device = f"http://{ip}:5000/{ungurl_upload}/from_another_device"

# Paths to save generated QR code images for download and upload links.
path_to_qr_download = "static/qr-code/download/qrcode.png"
path_to_qr_upload = "static/qr-code/upload/qrcode.png"

# Clear any existing QR code files or folders inside 'static/qr-code'.
qr_folder = Path("static/qr-code")
if qr_folder.exists() and qr_folder.is_dir():
    for file in qr_folder.iterdir():
        try:
            if file.is_file() or file.is_symlink():
                file.unlink()
            elif file.is_dir():
                shutil.rmtree(file)
        except Exception as e:
            pass

# Create directories to store QR codes if they do not exist yet.
os.makedirs("static/qr-code/download", exist_ok=True)
os.makedirs("static/qr-code/upload", exist_ok=True)

# Generate QR code images for the download and upload URLs and save them.
qr = qrcode.make(link_download)
qr.save(path_to_qr_download)
qr = qrcode.make(link_upload)
qr.save(path_to_qr_upload)

# Clear all files and folders inside the 'uploads' folder to start fresh.
clear_folder_contents("uploads")

# Define the upload folder path specific to the generated secure upload URL.
UPLOAD_FOLDER = f'uploads/{ungurl_upload}'

# Initialize Flask app and set the upload folder config.
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Print the upload link for easy access when running the server.
print(link_upload)

# Route for the main upload page with the secure URL.
# It renders an upload form and shows the generated access code and download links.
@app.route(f'/{ungurl}')
def index():
    return render_template("upload.html", code=code, link=link_download, link_another_device=link_another_device)

# Route for loading files from another device.
# Renders a page with links to download or upload from other devices.---------------------------------------------------------------
@app.route(f"/{ungurl_upload}/from_another_device")
def from_another_device():
    return render_template("load_from_other.html", link_download=link_download, link_upload=link_upload)

# API endpoint to check if the user entered the correct 6-digit code.
# Returns a JSON response indicating success or failure and lists uploaded files on success.
@app.route('/check_code', methods=['POST'])
def check_code():
    data = request.get_json()
    entered_code = data.get('code')

    # Compare entered code with the generated code (zero-padded).
    if entered_code and str(entered_code) == str(code).zfill(6):
        folder_path = app.config['UPLOAD_FOLDER']

        try:
            files = os.listdir(folder_path)
        except Exception as e:
            print(f"Error reading folder: {e}")
            files = []

        if not isinstance(files, list):
            files = []

        # Return success with list of files and download URL.
        return jsonify({
            'success': True,
            'download_link': f"/download/{ungurl_upload}",
            'files': files,
            'folder': ungurl_upload
        })
    else:
        print("Incorrect code entered")
        return jsonify({'success': False, 'error': 'Incorrect code! Please try again.'})

# Route to display the files available for download in the specific upload folder.
@app.route("/download/<ungurl_upload>")
def load(ungurl_upload):
    safe_folder = secure_filename(ungurl_upload)  # sanitize input for security
    folder_path = os.path.join(os.getcwd(), 'uploads', safe_folder)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        abort(404)  # Folder not found, send HTTP 404

    files = os.listdir(folder_path)
    return render_template('load.html', files=files, folder=safe_folder)

# Route to download a specific file from the upload folder.
@app.route('/download/<ungurl_upload>/<filename>')
def download(ungurl_upload, filename):
    safe_folder = secure_filename(ungurl_upload)
    safe_filename = secure_filename(filename)
    folder_path = os.path.join(os.getcwd(), 'uploads', safe_folder)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        abort(404)

    file_path = os.path.join(folder_path, safe_filename)
    if not os.path.exists(file_path):
        abort(404)

    # Send the file as an attachment so the browser downloads it.
    return send_from_directory(folder_path, safe_filename, as_attachment=True)

# Route to handle file uploads via POST request.
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        # Return error if no file part in the request
        return jsonify({'error': 'No file found'}), 400

    file = request.files['file']
    filename = file.filename

    if filename == '':
        # Return error if no file selected by user
        return jsonify({'error': 'No file selected'}), 400

    # Make sure upload folder exists before saving the file
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Save uploaded file to disk
    file.save(filepath)

    return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

# Route to delete a file from the upload folder.
@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.get_json()
    filename = data.get('filename')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'message': f'File {filename} deleted successfully.'}), 200
    else:
        # Return error if file does not exist
        return jsonify({'error': 'File not found'}), 404

# Main entry point: run Flask server on all interfaces at port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
