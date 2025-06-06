import os
import random
import secrets
import shutil
import string
from pathlib import Path
import re

from flask import Flask, render_template, jsonify, request, abort, send_from_directory, url_for
from werkzeug.utils import secure_filename
import qrcode

# Function to sanitize filenames by replacing unsafe characters with underscores
def sanitize_filename(filename):
    sanitized = re.sub(r'[^A-Za-z0-9._-]', '_', filename)
    return sanitized

# Function to generate a secure random string for download URLs
def generate_secure_code_download(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

# Function to generate a secure random string for upload URLs
def generate_secure_code_upload(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

# Function to clear all contents of a folder (files and subfolders)
def clear_folder_contents(folder_path):
    folder = Path(folder_path)
    if folder.exists() and folder.is_dir():
        for item in folder.iterdir():
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            except Exception:
                pass

# Function to get the base URL from the current request
def get_base_url():
    if request:
        return request.url_root.rstrip('/')
    return ''

# Generate secure random URLs for upload and download
ungurl = generate_secure_code_download(10)
ungurl_upload = generate_secure_code_upload(10)

# Define relative paths (will be combined with base URL later)
link_download = f"/download/{ungurl_upload}"
link_upload = f"/{ungurl}"
link_another_device = f"/{ungurl_upload}/from_another_device"

# Set paths for QR code images
path_to_qr_download = "static/qr-code/download/qrcode.png"
path_to_qr_upload = "static/qr-code/upload/qrcode.png"

# Clear any existing QR codes
qr_folder = Path("static/qr-code")
if qr_folder.exists() and qr_folder.is_dir():
    for file in qr_folder.iterdir():
        try:
            if file.is_file() or file.is_symlink():
                file.unlink()
            elif file.is_dir():
                shutil.rmtree(file)
        except Exception:
            pass

# Create directories for QR codes
os.makedirs("static/qr-code/download", exist_ok=True)
os.makedirs("static/qr-code/upload", exist_ok=True)

# Clear contents of uploads folder
clear_folder_contents("uploads")

# Set upload folder path with secure token
UPLOAD_FOLDER = f'uploads/{ungurl_upload}'

# Generate 6-digit access code
code = f"{random.randint(0, 999999):06d}"

# Initialize Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Generate QR codes on first request to ensure correct base URL
@app.before_first_request
def initialize_qr_codes():
    base_url = get_base_url()
    qr = qrcode.make(f"{base_url}{link_download}")
    qr.save(path_to_qr_download)
    qr = qrcode.make(f"{base_url}{link_upload}")
    qr.save(path_to_qr_upload)

@app.route('/')
def landing():
    base_url = get_base_url()
    return render_template("landing.html", link_another_device=(base_url + link_another_device), link_upload=(base_url + link_upload))

# Main upload page route
@app.route(f'/{ungurl}')
def index():
    return render_template("upload.html", code=code, link=link_download, link_another_device=link_another_device)

# Route for accessing from another device
@app.route(f"/{ungurl_upload}/from_another_device")
def from_another_device():
    return render_template("load_from_other.html", link_download=link_download, link_upload=link_upload)

# API endpoint to verify access code
@app.route('/check_code', methods=['POST'])
def check_code():
    data = request.get_json()
    entered_code = data.get('code')

    if entered_code and str(entered_code) == str(code).zfill(6):
        folder_path = app.config['UPLOAD_FOLDER']

        try:
            files = os.listdir(folder_path)
        except Exception:
            files = []

        return jsonify({
            'success': True,
            'download_link': link_download,
            'files': files,
            'folder': ungurl_upload
        })
    else:
        return jsonify({'success': False, 'error': 'Incorrect code! Please try again.'})

# Route to display available files for download
@app.route("/download/<ungurl_upload>")
def load(ungurl_upload):
    safe_folder = secure_filename(ungurl_upload)
    folder_path = os.path.join(os.getcwd(), 'uploads', safe_folder)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        abort(404)

    files = os.listdir(folder_path)
    safe_files = [sanitize_filename(f) for f in files]
    return render_template('load.html', files=safe_files, folder=safe_folder)

# Route to handle file downloads
@app.route('/download/<ungurl_upload>/<filename>')
def download(ungurl_upload, filename):
    safe_folder = secure_filename(ungurl_upload)
    safe_filename = sanitize_filename(filename)
    folder_path = os.path.join(os.getcwd(), 'uploads', safe_folder)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        abort(404)

    file_path = os.path.join(folder_path, safe_filename)
    if not os.path.exists(file_path):
        abort(404)

    return send_from_directory(folder_path, safe_filename, as_attachment=True)

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400

    file = request.files['file']
    filename = sanitize_filename(file.filename)

    if filename == '':
        return jsonify({'error': 'No file selected'}), 400

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)
    return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

# Route to handle file deletion
@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.get_json()
    filename = data.get('filename')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'message': f'File {filename} deleted successfully.'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404

# Start the Flask application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
