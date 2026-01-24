# 🎭 Face Recognition App

## Description
Multi-user face recognition application built with Python, Streamlit, and PostgreSQL.
Each user has their own isolated database for recognizing faces.

## Features
- ✅ **Multi-user authentication** (username/password with bcrypt)
- ✅ **User-isolated data** - each user has their own face database
- ✅ **Multiple face recognition** - detect multiple people in one image
- ✅ **Visual annotations** - colored boxes, arrows, and labels
- ✅ **Confirmation system** - verify recognition accuracy
- ✅ **EXIF orientation fix** - handles rotated images
- ✅ **100% local or cloud** - SQLite for local, PostgreSQL for production
- ✅ **GDPR compliant**

## Technologies
- Python 3.11+
- Streamlit (UI)
- face_recognition (dlib-based)
- PostgreSQL / SQLite (database)
- bcrypt (password hashing)
- OpenCV, NumPy, Pillow

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

##  Local Installation - DETAILED (Mac/Linux or Virtual Environment)

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

## ☁️ Deployment to Streamlit Cloud

### 1. Push to GitHub
```bash
git add .
git commit -m "Add multi-user authentication"
git push
```

### 1. Create PostgreSQL Database
Go to [Neon](https://neon.tech/) or [Supabase](https://supabase.com/) and create a free PostgreSQL database.

### 2. Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Connect your GitHub repository
3. Select main file: `app.py`
4. Add **Secrets** (in Advanced Settings):
```toml
DATABASE_URL = "postgresql://user:password@host:port/database"
```

### 3. Done! 🎉
Your app is now live and accessible to anyone with the URL.

---

## 🔐 Security Notes

- **Passwords are hashed with bcrypt** - never stored in plain text
- **Each user has isolated data** - user_1 cannot see user_2's faces
- **PostgreSQL on Streamlit Cloud** - automatic backups and SSL
- **SQLite for local dev** - no database setup needed

---

## ⚠️ Important Notes

### GDPR & Privacy
- **The `data/` folder contains user data!**
- Never commit `data/users/` to GitHub
- Only store images with consent
- Add `data/users/` to `.gitignore`

---

## 📄 License
MIT License - Educational project

## 🤝 Contributing
Pull requests and issues are welcome!
