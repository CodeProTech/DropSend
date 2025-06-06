# DropSend

📡 **DropSend** – Quickly and easily send files and texts over your local network.

With DropSend, you can transfer files, texts, or images between any devices connected to the **same Wi-Fi or LAN** – completely without the Internet or cloud! Just open the link in your browser and start exchanging files.

---

## 🚀 Features

* 🌐 Device connection over local network (Wi-Fi/LAN)
* 🔒 No internet transmission – 100% local
* 📁 Supports all file types (PDFs, images, ZIPs, etc.)
* 📲 Compatible with smartphone, tablet, PC, Mac, and more
* 🖼️ Drag & drop upload
* 📤 Upload files from any device in the same network
* 📥 Instantly download all uploaded files in the browser
* 🔐 Access protected by 6-digit security code
* 📦 QR codes for upload & download links
* ❌ Option to delete uploaded files

---

## 📸 Demo Screenshot

<img src="https://github.com/user-attachments/assets/a4a52509-9091-4b00-aa22-7999c3a52bf4" alt="DropSend Demo Screenshot" width="600" />

---

## 🎥 Demo Video
<p>Watch DropSend in action:</p>
<a href="https://www.youtube.com/watch?v=E_6drOP1is8" target="_blank">
  <img src="https://img.youtube.com/vi/E_6drOP1is8/0.jpg" alt="DropSend Demo Video" width="320" height="180" />
</a>
<p>➡️ <a href="https://www.youtube.com/watch?v=E_6drOP1is8" target="_blank">Watch it on YouTube</a></p>

---

## 🖥️ Compatibility

Works on **all devices** with a web browser:

| Device                   | Supported  |
| ------------------------ | ---------- |
| Windows PC               | ✅          |
| Mac                      | ✅          |
| Linux                    | ✅          |
| iPhone/iPad              | ✅          |
| Android                  | ✅          |
| Smart TVs (with browser) | ⚠️ Partial |

All devices must be on the **same local network** (e.g. via Wi-Fi).

---

## 🧩 Installation

### 1. Requirements

- **Git** (to clone the repository)
- **Python** 3.8 or higher  
- **Pip packages**:
  - `flask`
  - `qrcode`

### 2. Install

```bash
git clone https://github.com/CodeProTech/DropSend
```

```bash
cd DropSend
```

```bash
pip install -r requirements.txt
```

```bash
pip install flask qrcode
```

### 3. Run the App

```bash
python main.py
```

✅ A browser window will open automatically with your private upload link.

---

## 📱 Usage

### Send from PC

1. Make sure your device is on the same Wi-Fi network as your PC.
2. Upload one or more files using the file browser or drag & drop.
3. Scan the QR code or open the link on your other device (e.g. `http://192.168.178.45:5000/abc123xyz`).
4. Enter the 6-digit code shown on your PC.

✅ Now download the uploaded files on your other device.

### Send from Another Device

1. Make sure your device is on the same Wi-Fi network as your PC.
2. Open the link with the text "transfer files and photos from another device."
3. Scan the QR code or open the link on your other device (e.g. `http://192.168.178.45:5000/abc123xyz`).
4. Upload one or more files using the file browser or drag & drop.
5. Scan the QR code or open the link again if needed.
6. Enter the 6-digit code shown on your device.

✅ Now download the uploaded files on your other device.

---

## ⚠️ Security & Notes

* DropSend is not accessible via the Internet – only in the local network.
* Upload/download links are protected by random codes (e.g. `abc123xyz`).
* The upload folder is automatically cleared at startup.

---

## ✅ Todo & Ideas for the Future

* Expiration time for links
* Enhanced security
* Direct file sending between devices in the network

---

## 👨‍💻 Author

Stefanos Koufogazos Loukianov

---

## 📬 Contact

Email: [stefanoskoufogazos@outlook.com](mailto:stefanoskoufogazos@outlook.com)

---

## 📝 License

MIT License
