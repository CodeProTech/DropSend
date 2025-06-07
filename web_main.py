import os
import random
import secrets
import shutil
import string
from pathlib import Path
import re
import time
from datetime import datetime, timedelta
from threading import Timer
from flask import Flask, render_template, jsonify, request, abort, send_from_directory, url_for
from werkzeug.utils import secure_filename
import qrcode

# Store active sessions with their expiration times
# Format: {ungurl_upload: {'expires': timestamp, 'code': code, 'upload_folder': folder_path}}
active_sessions = {}

# Expiration time in seconds (15 minutes)
EXPIRATION_TIME = 15 * 60


# Function to sanitize filenames by replacing unsafe characters with underscores
def sanitize_filename(filename):
    sanitized = re.sub(r'[^A-Za-z0-9._-]', '_', filename)
    return sanitized


def cleanup_expired_sessions():
    """Remove expired sessions and their folders"""
    current_time = time.time()
    expired_sessions = [
        ungurl for ungurl, data in active_sessions.items()
        if data['expires'] < current_time
    ]

    for ungurl in expired_sessions:
        try:
            # Remove the upload folder
            folder_path = active_sessions[ungurl]['upload_folder']
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

            # Remove session data
            del active_sessions[ungurl]
        except Exception as e:
            print(f"Error cleaning up session {ungurl}: {e}")


def schedule_cleanup():
    """Schedule periodic cleanup of expired sessions"""
    cleanup_expired_sessions()
    # Schedule next cleanup in 5 minutes
    Timer(300, schedule_cleanup).start()


# Function to generate a secure random string for download URLs
def generate_secure_code_download(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


# Function to generate a secure random string for upload URLs
def generate_secure_code_upload(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


# Function to get the base URL from the current request
def get_base_url():
    if request:
        return request.url_root.rstrip('/')
    return ''


# Initialize Flask application
app = Flask(__name__)

# Start the cleanup scheduler
schedule_cleanup()


@app.route('/')
def landing():
    # Generate new unique URLs for this session
    ungurl_upload = generate_secure_code_upload(10)
    ungurl = generate_secure_code_download(10)
    code = f"{random.randint(0, 999999):06d}"
    upload_folder = f'uploads/{ungurl_upload}'

    # Store session data
    active_sessions[ungurl_upload] = {
        'expires': time.time() + EXPIRATION_TIME,
        'code': code,
        'upload_folder': upload_folder,
        'ungurl': ungurl
    }

    # Clear contents of the new upload folder
    os.makedirs(upload_folder, exist_ok=True)
    clear_folder_contents(upload_folder)

    # Generate QR codes
    base_url = get_base_url()
    link_another_device = f"/{ungurl_upload}/from_another_device"
    link_upload = f"/{ungurl}"

    # Create QR code directories
    os.makedirs("static/qr-code/download", exist_ok=True)
    os.makedirs("static/qr-code/upload", exist_ok=True)

    # Generate QR codes
    qr = qrcode.make(f"{base_url}/download/{ungurl_upload}")
    qr.save(f"static/qr-code/download/{ungurl_upload}.png")
    qr = qrcode.make(f"{base_url}{link_upload}")
    qr.save(f"static/qr-code/upload/{ungurl_upload}.png")

    return render_template(
        "landing.html",
        link_another_device=(base_url + link_another_device),
        link_upload=(base_url + link_upload)
    )


@app.route('/<ungurl>')
def index(ungurl):
    # Find the session for this ungurl
    session = None
    for sess_data in active_sessions.values():
        if sess_data.get('ungurl') == ungurl:
            session = sess_data
            break

    if not session or session['expires'] < time.time():
        return "Link expired or invalid", 404

    link_download = f"/download/{ungurl}"
    link_another_device = f"/{ungurl}/from_another_device"

    return render_template(
        "upload.html",
        code=session['code'],
        link=link_download,
        link_another_device=link_another_device
    )


@app.route("/<ungurl_upload>/from_another_device")
def from_another_device(ungurl_upload):
    if ungurl_upload not in active_sessions or active_sessions[ungurl_upload]['expires'] < time.time():
        return "Link expired or invalid", 404

    session = active_sessions[ungurl_upload]
    link_download = f"/download/{ungurl_upload}"
    link_upload = f"/{session['ungurl']}"

    return render_template(
        "load_from_other.html",
        link_download=link_download,
        link_upload=link_upload
    )


@app.route('/check_code', methods=['POST'])
def check_code():
    data = request.get_json()
    entered_code = data.get('code')

    # Find the active session for this code
    session = None
    ungurl_upload = None
    for key, sess_data in active_sessions.items():
        if sess_data['code'] == entered_code:
            session = sess_data
            ungurl_upload = key
            break

    if not session or session['expires'] < time.time():
        return jsonify({'success': False, 'error': 'Invalid or expired code'})

    try:
        files = os.listdir(session['upload_folder'])
    except Exception:
        files = []

    return jsonify({
        'success': True,
        'download_link': f"/download/{ungurl_upload}",
        'files': files,
        'folder': ungurl_upload
    })


@app.route("/download/<ungurl_upload>")
def load(ungurl_upload):
    if ungurl_upload not in active_sessions or active_sessions[ungurl_upload]['expires'] < time.time():
        return "Link expired or invalid", 404

    session = active_sessions[ungurl_upload]
    folder_path = session['upload_folder']

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        abort(404)

    files = os.listdir(folder_path)
    safe_files = [sanitize_filename(f) for f in files]
    return render_template('load.html', files=safe_files, folder=ungurl_upload)


@app.route('/download/<ungurl_upload>/<filename>')
def download(ungurl_upload, filename):
    if ungurl_upload not in active_sessions or active_sessions[ungurl_upload]['expires'] < time.time():
        return "Link expired or invalid", 404

    session = active_sessions[ungurl_upload]
    safe_filename = sanitize_filename(filename)
    folder_path = session['upload_folder']

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        abort(404)

    file_path = os.path.join(folder_path, safe_filename)
    if not os.path.exists(file_path):
        abort(404)

    return send_from_directory(folder_path, safe_filename, as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400

    file = request.files['file']
    filename = sanitize_filename(file.filename)

    if filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Find the active session based on the code or URL
    session = None
    for sess_data in active_sessions.values():
        if sess_data['expires'] > time.time():
            session = sess_data
            break

    if not session:
        return jsonify({'error': 'No active session found'}), 400

    upload_folder = session['upload_folder']
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)
    return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200


@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.get_json()
    filename = data.get('filename')

    # Find the active session that contains the file
    session = None
    for sess_data in active_sessions.values():
        filepath = os.path.join(sess_data['upload_folder'], filename)
        if os.path.exists(filepath):
            session = sess_data
            break

    if not session or session['expires'] < time.time():
        return jsonify({'error': 'File not found or session expired'}), 404

    filepath = os.path.join(session['upload_folder'], filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'message': f'File {filename} deleted successfully.'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404


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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
