<<<<<<< HEAD
# 🖼️ Background Remover API

This is a Flask-based API for removing image backgrounds using the powerful [rembg](https://github.com/danielgatis/rembg) library. It supports multiple models optimized for general use, high-quality rendering, human portraits, and lightweight performance.

> ⚙️ Built for local usage and Google Colab deployments with public API exposure using `ngrok`.

---

## 🚀 Features

- ✅ Upload an image and remove the background via API.
- 🎯 Choose from 4 pre-trained models:
  - `general` – U2-Net (default)
  - `high_quality` – IS-Net
  - `human` – Silueta
  - `light` – U2-Net-P
- 📤 Returns result as base64-encoded image + downloadable PNG.
- 🧹 Cleans up temporary files older than 1 hour automatically.
- 🌐 Deployable in Google Colab using `pyngrok` for public access.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Lalelani-Eddie/background-remover-api.git
cd background-remover-api
````

### 2. Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

### 🔹 Locally:

```bash
python app.py
```

Visit: `http://localhost:5000`

---

### 🔹 In Google Colab (Public API):

Install dependencies in Colab:

```python
!pip install flask pyngrok rembg
```

At the end of your script, add:

```python
from pyngrok import ngrok
from threading import Thread

ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")  # Replace with your token

public_url = ngrok.connect(5000)
print(f"🚀 Public URL: {public_url}")

def run_app():
    app.run(port=5000)

Thread(target=run_app).start()
```

---

## 📤 API Endpoints

### `POST /upload`

Upload an image and receive a background-removed result.

#### Parameters:

* `file` — Image file (jpg, png, etc.)
* `model` (optional) — One of: `general`, `high_quality`, `human`, `light`

#### Sample Request (Python):

```python
import requests

url = "https://your-ngrok-url.ngrok.io/upload"
files = {'file': open('test.jpg', 'rb')}
data = {'model': 'general'}

res = requests.post(url, files=files, data=data)
print(res.json())
```

---

### `GET /api/models`

Returns a list of available background removal models.

---

### `GET /download/<filename>`

Downloads the processed image as a PNG with a transparent background.

---

## 🗂️ Project Structure

```
.
├── app.py               # Main Flask application
├── uploads/             # Temporary uploaded images
├── processed/           # Processed output files
├── requirements.txt     # Dependencies
└── README.md
```

---

## 👤 Author

**Lalelani Eddie Nene**
🔗 [GitHub Profile](https://github.com/yourusername)
📬 Contact: +27 64 421 0047

---

## 🛡 License

This project is licensed under the **MIT License**.

---

> ✨ Feel free to fork, use, or contribute to the project. Happy background removing!

```

---
=======
# Background-Remover
The app to remove the background
>>>>>>> 77db3986c599ed8735f90d9d7631a71d2e66fd62
