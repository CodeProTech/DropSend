Drop Send

Drop Send is a simple and fast file transfer application that allows users to send files securely between devices or to share them with others. With its easy-to-use interface and strong encryption, Drop Send is designed to make file sharing faster and safer.
Features

    Fast File Transfer: Send files between devices in seconds, regardless of size.

    Secure Encryption: All files are transferred using secure encryption to protect your privacy.

    Cross-Platform: Compatible with multiple platforms (Windows, macOS, Linux).

    Drag-and-Drop Interface: Easily select files to send using the drag-and-drop feature.

    No Signup Required: Start sending files instantly without needing to sign up or log in.

    Notifications: Get real-time notifications when a file transfer is complete.

Installation
Requirements

    Python 3.x

    Flask (for web interface)

    Other dependencies: pip install -r requirements.txt (includes libraries like requests, pycryptodome for encryption, etc.)

Steps to Install

    Clone this repository:

git clone https://github.com/yourusername/dropsend.git
cd dropsend

Create a virtual environment (optional, but recommended):

python3 -m venv .venv

Install the required dependencies:

pip install -r requirements.txt

Run the application:

    python app.py

    This will start a local server, and you can open your browser to http://127.0.0.1:5000 to use the app.

Usage

    Open the app in your browser.

    Drag and drop the file(s) you want to send into the designated area.

    Enter the recipient’s email or device ID (if required), and hit Send.

    The recipient will receive a link to download the file.

    Optionally, you can set an expiration time for the file link.

Contributing

We welcome contributions to Drop Send! If you'd like to improve the project, please fork the repository and submit a pull request.
How to Contribute:

    Fork the repository on GitHub.

    Create a new branch for your changes.

    Make your changes and commit them.

    Push your changes to your forked repository.

    Open a pull request.

Please ensure your changes adhere to the project's coding standards and include tests where applicable.
License

This project is licensed under the MIT License - see the LICENSE file for details.
Contact

For any questions or suggestions, please feel free to reach out to us at:

    Email: contact@dropsend.com

    GitHub: https://github.com/yourusername/dropsend
