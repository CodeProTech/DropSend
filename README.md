# DropSend

📡 DropSend – Dateien und Texte schnell und einfach über dein lokales Netzwerk senden.

Mit DropSend kannst du Dateien, Texte oder Bilder zwischen allen Geräten übertragen, die sich im **selben WLAN oder LAN** befinden – ganz ohne Internet oder Cloud! Öffne einfach den Link im Browser und schon kannst du Dateien austauschen.

---

## 🚀 Features

- 🌐 Geräteverbindung über das lokale Netzwerk (WLAN/LAN)
- 🔒 Keine Datenübertragung übers Internet – 100 % lokal
- 📁 Unterstützt alle Dateiarten (PDF, Bilder, ZIPs usw.)
- 📲 Kompatibel mit Smartphone, Tablet, PC, Mac usw.
- 🖼️ Drag & Drop Upload
- 📤 Dateien von jedem Gerät im gleichen WLAN hochladen
- 📥 Alle hochgeladenen Dateien sofort im Browser herunterladen
- 🔐 Zugriff nur über 6-stelligen Sicherheitscode
- 📦 QR-Codes für Upload- & Download-Links
- ❌ Unterstützt auch Löschen hochgeladener Dateien

---

## 🖥️ Kompatibilität

Funktioniert auf **allen Geräten** mit einem Webbrowser:

| Gerät | Unterstützt |
|------|-------------|
| Windows-PC | ✅
| Mac | ✅
| Linux | ✅
| iPhone/iPad | ✅
| Android | ✅
| Smart TVs (mit Browser) | ⚠️ teilweise 

Alle Geräte müssen im **selben lokalen Netzwerk** sein (z. B. über WLAN verbunden).

---

## 🧩 Installation

### 1. Voraussetzungen

- Python 3.8+
- Pip-Pakete: `flask`, `qrcode`

### 2. Installation

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
pip install flask, qrcode
```

### 3. Anwendung

```bash
python main.py
```
✅ Ein Browserfenster öffnet sich automatisch mit deinem privaten Upload-Link.

---

## (emojie )Anwendung 
### Sende von PC
1. Vergewissere dich, dass dein Gerät im selben WLAN ist wie dein PC.
2. Lade eine oder mehrere datein hoch durch browse oder drag and drop
3. Scane nun den qrcode oder gib den link auf deinem anderen gerät ein (link bsp. `http://192.168.178.45:5000/abc123xyz`)
4. Gib den 6-Stelligen code der auf deinem pc angezeigt wird ein

✅ Lade nun deine hochgeladenen datein auf deinem anderen geräd runter

### Sende von einem anderen Gerät
1. Vergewissere dich, dass dein Gerät im selben WLAN ist wie dein PC.
2. Öffne den link mit dem text "transfer files and photos from another device"
3. Scane nun den qrcode oder gib den link auf deinem anderen gerät ein (link bsp. `http://192.168.178.45:5000/abc123xyz`)
4. Lade eine oder mehrere datein hoch durch browse oder drag and drop
5. Scane nun den qrcode oder gib den link auf deinem anderen gerät ein (link bsp. `http://192.168.178.45:5000/abc123xyz`)
6. Gib den 6-Stelligen code der auf deinem pc angezeigt wird ein

✅ Lade nun deine hochgeladenen datein auf deinem anderen geräd runter

---

## ⚠️ Sicherheit & Hinweise

- DropSend ist nicht über das Internet erreichbar – nur im lokalen Netzwerk.
- Die Links sind mit zufälligen Codes geschützt (z. B. abc123xyz).
- Der Upload-Ordner wird beim Start automatisch gelöscht.

---

## ✅ Todo & Ideen für die Zukunft
- ABlaufszeit der links
- noch sicherer
- direktes schicken der datein zu geräten im  netwerk
---

## 👨‍💻 Autor
Stefanos Koufogazos Loukianov

---

## Kontakt
Email: [stefanoskoufogazos@outlook.com](stefanoskoufogazos@outlook.com)


---

## 📝 Lizenz

MIT License – kostenlos nutzbar, auch kommerziell.
