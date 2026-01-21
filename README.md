# 🎭 Face Recognition App

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## Description
Local face recognition application built with Python and Streamlit UI.
Learning project following Best Practices, OOP principles, and PEP 8 standards.

## 🌐 Live Demo
**👉 [Try it here!](https://your-app-name.streamlit.app)**

## Features
- ✅ 100% local, GDPR compliant
- ✅ OOP architecture with Type Hinting
- ✅ Professional logging
- ✅ Modular structure
- ✅ Streamlit Cloud deployment ready

## Technologies
- Python 3.11+
- Streamlit
- face_recognition (dlib-based)
- OpenCV
- NumPy, Pillow

---

## ⚡ QUICK INSTALL - FOR WINDOWS USERS

**THE EASIEST METHOD:**

### 1️⃣ Double-click this file:
```
install_windows.bat
```

**Done! 🎉** This automatically installs everything (using pre-compiled dlib-bin)

---

### 🛠️ Or Manually (3 commands):

```bash
pip install dlib-bin
pip install --no-deps face-recognition
pip install -r requirements-windows.txt
```

### ▶️ Run:
```bash
streamlit run app.py
```

**🌐 Browser opens automatically at: `http://localhost:8501`**

---

## 🚀 Streamlit Cloud Deployment (ONLINE)

### 1. Fork or Clone this repo
```bash
git clone https://github.com/YOUR_USERNAME/FaceRecognitionApp.git
```

### 2. Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 3. Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"** button
4. Select:
   - Repository: `YOUR_USERNAME/FaceRecognitionApp`
   - Branch: `main`
   - Main file: `app.py`
5. Click **"Deploy!"**

⏱️ **First deployment takes ~5-10 minutes** (due to dlib compilation)

---

## 💻 Local Installation - DETAILED (Mac/Linux or Virtual Environment)

### Option A: Virtual Environment (recommended for production)

```bash
# 1. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

### Option B: Global installation (quick test)

**Windows:**
```bash
pip install -r requirements-windows.txt
streamlit run app.py
```

**Mac/Linux:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📸 Usage

### 1. Prepare your data
Place images in the `data/people/` folder, with separate subfolders for each person:
```
data/people/
├── Person_A/
│   ├── photo1.jpg
│   └── photo2.jpg
└── Person_B/
    └── photo1.jpg
```

### 2. Build database
- The app automatically loads images at startup
- Or click the **"🔄 Rebuild Database"** button in the sidebar

### 3. Recognize faces
- Upload an image in the app
- The app will try to recognize faces

---

## 📁 Project Structure
```
FaceRecognitionApp/
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── src/                    # Source code modules
│   ├── data_manager.py    # Face database manager
│   ├── face_engine.py     # Face recognition engine
│   └── utils.py           # Utility functions
├── data/                   # Local data storage
│   ├── people/            # Person folders (gitignored!)
│   ├── encodings/         # Cache files
│   └── logs/              # Log files
├── config.py              # Central configuration
├── app.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── packages.txt           # Linux system packages (Streamlit Cloud)
└── .gitignore            # Git exclusions
```

---

## 🛠️ Development

### Code Quality
```bash
# Formatting
black src/ app.py config.py

# Linting
flake8 src/ app.py config.py

# Type checking
mypy src/ app.py config.py
```

### Testing
```bash
pytest tests/
```

---

## ⚠️ Important Notes

### GDPR & Privacy
- **The `data/people/` folder is in .gitignore!**
- Never commit personal face images
- Only store production images on your local machine

### Streamlit Cloud Limitations
- **Free tier:** 1 GB RAM, 1 CPU
- **Timeout:** Goes to sleep after 10 minutes of inactivity
- **Not recommended:** For large databases (>100 people)

---

## 📄 License
MIT License - Educational project

## 🤝 Contributing
Pull requests and issues are welcome!
