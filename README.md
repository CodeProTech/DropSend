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

## 🌐 Local & Online Version Available

DropSend is now available not only for local use (via Wi-Fi/LAN), but also as an online version for broader accessibility!

🔗 Try the Online Demo here:
👉 [https://dropsend.onrender.com](https://dropsend.onrender.com/)

> ⚠️ **Note:** This version does not use your local network – it is intended for testing or online file sharing.

---

## 📸 Demo Screenshot

<img src="https://github.com/user-attachments/assets/49a5b8cf-81d1-477c-b731-597bd68f85b3" alt="DropSend Demo Screenshot" width="600" />

---
## 🎥 DropSend – New Demo (2025)

🚀 **Check out the latest version! Watch the updated demo with all improvements:**

[![DropSend New Version](https://img.youtube.com/vi/nEDPa_jXrcA/0.jpg)](https://www.youtube.com/watch?v=nEDPa_jXrcA)

👉 [Watch on YouTube](https://www.youtube.com/watch?v=nEDPa_jXrcA)

> ⚠️ **Note:** The <a href="https://www.youtube.com/watch?v=E_6drOP1is8" target="_blank">old demo </a> is still available.
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

## 🙌 Support the Project

> ⭐️ **If you like DropSend, feel free to leave a star on GitHub! It really helps the project grow. Thanks a lot!**

---

## 👨‍💻 Author

Stefanos Koufogazos Loukianov

---

## 📬 Contact

Email: [stefanoskoufogazos@outlook.com](mailto:stefanoskoufogazos@outlook.com)

---

## 📝 License

MIT License
