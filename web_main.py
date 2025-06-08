import os
import random
import secrets
import shutil
import string
from pathlib import Path
import re
from datetime import datetime, timedelta

from flask import Flask, render_template, jsonify, request, abort, send_from_directory, url_for, session
from werkzeug.utils import secure_filename
import qrcode
from PIL import Image


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


# Dictionary to store active sessions and their data
active_sessions = {}


def create_user_session():
    """Create a new user session with unique identifiers and links"""
    # Generate base data
    ungurl = generate_secure_code_download(10)
    ungurl_upload = generate_secure_code_upload(10)
    code = f"{random.randint(0, 999999):06d}"
    created_at = datetime.now()
    session_id = secrets.token_urlsafe(32)

    # Create session data with links
    session_data = {
        'session_id': session_id,
        'ungurl': ungurl,
        'ungurl_upload': ungurl_upload,
        'code': code,
        'created_at': created_at.isoformat(),
        'link_download': f"/download/{ungurl_upload}",
        'link_upload': f"/{ungurl}",
        'link_another_device': f"/{ungurl_upload}/from_another_device"
    }

    return session_data

def generate_session_qr_codes(user_data, base_url):
    """Generate and save QR codes for a specific session"""
    try:
        # Create session-specific QR code directories
        download_dir = Path("static/qr-code/download")
        upload_dir = Path("static/qr-code/upload")
        download_dir.mkdir(parents=True, exist_ok=True)
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Generate QR codes with full URLs
        download_url = f"{base_url}{user_data['link_download']}"
        upload_url = f"{base_url}{user_data['link_upload']}"

        # Create and save download QR code
        qr_download = qrcode.make(download_url)
        qr_download_path = download_dir / f"{user_data['ungurl_upload']}.png"
        qr_download.save(str(qr_download_path))

        # Create and save upload QR code
        qr_upload = qrcode.make(upload_url)
        qr_upload_path = upload_dir / f"{user_data['ungurl']}.png"
        qr_upload.save(str(qr_upload_path))

        return {
            'qr_download': f"static/qr-code/download/{user_data['ungurl_upload']}.png",
            'qr_upload': f"static/qr-code/upload/{user_data['ungurl']}.png"
        }
    except Exception as e:
        print(f"Error generating QR codes: {e}")
        return {
            'qr_download': '',
            'qr_upload': ''
        }


def cleanup_expired_sessions():
    """Remove expired sessions and their associated files"""
    current_time = datetime.now()
    expired = []
    for session_id, data in active_sessions.items():
        created_at = datetime.fromisoformat(data['created_at'])
        if current_time - created_at > timedelta(minutes=15):
            expired.append(session_id)
            # Clean up uploaded files
            folder_path = f'uploads/{data["ungurl_upload"]}'
            clear_folder_contents(folder_path)
            try:
                shutil.rmtree(folder_path)
                # Clean up QR codes
                download_qr = Path(f"static/qr-code/download/{data['ungurl_upload']}.png")
                upload_qr = Path(f"static/qr-code/upload/{data['ungurl']}.png")
                if download_qr.exists():
                    download_qr.unlink()
                if upload_qr.exists():
                    upload_qr.unlink()
            except Exception:
                pass

    for session_id in expired:
        del active_sessions[session_id]

def is_session_valid(ungurl_upload):
    """Check if a session is valid and not expired"""
    current_time = datetime.now()
    for data in active_sessions.values():
        if data['ungurl_upload'] == ungurl_upload:
            created_at = datetime.fromisoformat(data['created_at'])
            if current_time - created_at <= timedelta(minutes=15):
                return True
    return False

# Initialize Flask application
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate a secure secret key

# Create required directories
os.makedirs("static/qr-code/download", exist_ok=True)
os.makedirs("static/qr-code/upload", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

# Clear contents on startup
clear_folder_contents("uploads")
clear_folder_contents("static/qr-code/download")
clear_folder_contents("static/qr-code/upload")


@app.before_request
def check_session():
    """Check and clean up sessions before each request"""
    cleanup_expired_sessions()

    # Check if session exists and is valid
    if 'user_data' in session:
        user_data = session['user_data']
        # Convert stored ISO format string to datetime
        created_at = datetime.fromisoformat(user_data['created_at'])
        # Check if session has expired (more than 15 minutes old)
        if datetime.now() - created_at > timedelta(minutes=15):
            # Remove old session
            if user_data['session_id'] in active_sessions:
                del active_sessions[user_data['session_id']]
            # Create new session
            user_data = create_user_session()
            session['user_data'] = user_data
            active_sessions[user_data['session_id']] = user_data
    else:
        # Create new session if none exists
        user_data = create_user_session()
        session['user_data'] = user_data
        active_sessions[user_data['session_id']] = user_data

@app.route('/')
def landing():
    """Landing page route"""
    user_data = session.get('user_data')
    if not user_data:
        user_data = create_user_session()
        session['user_data'] = user_data
        active_sessions[user_data['session_id']] = user_data

    base_url = get_base_url()
    qr_paths = generate_session_qr_codes(user_data, base_url)

    return render_template("landing.html",
                           link_another_device=(base_url + user_data['link_another_device']),
                           link_upload=(base_url + user_data['link_upload']),
                           qr_download=qr_paths['qr_download'],
                           qr_upload=qr_paths['qr_upload'])


@app.route('/<ungurl>')
def index(ungurl):
    """Upload page route"""
    for session_data in active_sessions.values():
        if session_data['ungurl'] == ungurl:
            # Convert the ISO format string back to datetime
            created_at = datetime.fromisoformat(session_data['created_at'])
            if datetime.now() - created_at <= timedelta(minutes=15):
                base_url = get_base_url()

                qr_paths = generate_session_qr_codes(session_data, base_url)

                return render_template("upload.html",
                                   ungurl_download=session_data['ungurl_upload'],
                                   code=session_data['code'],
                                   link=session_data['link_download'],
                                   link_another_device=session_data['link_another_device'],
                                   qr_download=qr_paths['qr_download'])

    abort(410)  # Gone - Session expired

@app.route("/<ungurl_upload>/from_another_device")
def from_another_device(ungurl_upload):
    """Route for accessing from another device"""
    if not is_session_valid(ungurl_upload):
        abort(410)  # Gone - Session expired

    for session_data in active_sessions.values():
        if session_data['ungurl_upload'] == ungurl_upload:
            return render_template("load_from_other.html",
                                   ungurl=session_data['ungurl'],
                                   link_download=session_data['link_download'],
                                   link_upload=session_data['link_upload'])

    abort(404)


@app.route('/check_code', methods=['POST'])
def check_code():
    """API endpoint to verify access code"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        entered_code = data.get('code')
        if not entered_code:
            return jsonify({'success': False, 'error': 'No code provided'}), 400

        for session_data in active_sessions.values():
            if str(entered_code) == str(session_data['code']).zfill(6):
                created_at = datetime.fromisoformat(session_data['created_at'])
                if datetime.now() - created_at <= timedelta(minutes=15):
                    folder_path = f"uploads/{session_data['ungurl_upload']}"

                    try:
                        files = os.listdir(folder_path) if os.path.exists(folder_path) else []
                    except Exception:
                        files = []

                    return jsonify({
                        'success': True,
                        'download_link': session_data['link_download'],
                        'files': files,
                        'folder': session_data['ungurl_upload']
                    })

        return jsonify({
            'success': False,
            'error': 'Incorrect code! Please try again.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route("/download/<ungurl_upload>")
def load(ungurl_upload):
    """Route to display available files for download"""
    if not is_session_valid(ungurl_upload):
        abort(410)  # Gone - Session expired

    safe_folder = secure_filename(ungurl_upload)
    folder_path = os.path.join(os.getcwd(), 'uploads', safe_folder)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        abort(404)

    files = os.listdir(folder_path)
    safe_files = [sanitize_filename(f) for f in files]
    return render_template('load.html', files=safe_files, folder=safe_folder)


@app.route('/download/<ungurl_upload>/<filename>')
def download(ungurl_upload, filename):
    """Route to handle file downloads"""
    try:
        if not is_session_valid(ungurl_upload):
            return jsonify({'error': 'Session expired'}), 410

        safe_folder = secure_filename(ungurl_upload)
        safe_filename = sanitize_filename(filename)
        folder_path = os.path.join(os.getcwd(), 'uploads', safe_folder)

        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return jsonify({'error': 'File not found'}), 404

        file_path = os.path.join(folder_path, safe_filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        return send_from_directory(
            folder_path,
            safe_filename,
            as_attachment=True,
            download_name=safe_filename  # Ensure proper filename encoding
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    """Route to handle file uploads"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400

    if 'user_data' not in session:
        return jsonify({'error': 'Session expired'}), 410

    file = request.files['file']
    filename = sanitize_filename(file.filename)

    if filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Use session-specific upload folder
    upload_folder = f"uploads/{session['user_data']['ungurl_upload']}"
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)
    return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200


@app.route('/delete', methods=['POST'])
def delete_file():
    """Route to handle file deletion"""
    if 'user_data' not in session:
        return jsonify({'error': 'Session expired'}), 410

    data = request.get_json()
    filename = data.get('filename')
    upload_folder = f"uploads/{session['user_data']['ungurl_upload']}"
    filepath = os.path.join(upload_folder, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'message': f'File {filename} deleted successfully.'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404


@app.errorhandler(410)
def session_expired(error):
    """Error handler for expired sessions"""
    return render_template('error.html',
                           error_code=410,
                           error_message="This session has expired. Please start a new session."), 410


@app.errorhandler(404)
def not_found(error):
    """Error handler for not found resources"""
    return render_template('error.html',
                           error_code=404,
                           error_message="The requested resource was not found."), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

