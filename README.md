# 🎭 Face Recognition App

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## Leírás
Lokális arcfelismerő alkalmazás Python-ban, Streamlit UI-val. 
Tanulási projekt - Best Practices, OOP, PEP 8 szabványokkal.

## 🌐 Live Demo
**👉 [Próbáld ki itt!](https://your-app-name.streamlit.app)**

## Jellemzők
- ✅ 100% lokális, GDPR konform
- ✅ OOP architektúra, Type Hinting
- ✅ Professzionális logging
- ✅ Moduláris felépítés
- ✅ Streamlit Cloud deployment ready

## Technológiák
- Python 3.11+
- Streamlit
- face_recognition (dlib alapú)
- OpenCV
- NumPy, Pillow

---

## 🚀 Streamlit Cloud Deployment

### 1. Fork vagy Clone ez a repo
```bash
git clone https://github.com/YOUR_USERNAME/FaceRecognitionApp.git
```

### 2. Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 3. Deploy Streamlit Cloud-ra
1. Menj a [share.streamlit.io](https://share.streamlit.io)
2. Jelentkezz be GitHub accounttal
3. Kattints a **"New app"** gombra
4. Válaszd ki:
   - Repository: `YOUR_USERNAME/FaceRecognitionApp`
   - Branch: `main`
   - Main file: `app.py`
5. Kattints **"Deploy!"**

⏱️ **Az első deployment ~5-10 percet vesz igénybe** (dlib fordítása miatt)

---

## 💻 Lokális Telepítés

### Windows (Könnyített verzió)

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/FaceRecognitionApp.git
cd FaceRecognitionApp

# 2. Telepítsd a dlib-bin-t (előre fordított)
pip install dlib-bin
pip install --no-deps face-recognition
pip install face-recognition-models

# 3. Telepítsd a többi csomagot
pip install streamlit opencv-python numpy pillow

# 4. Futtasd
streamlit run app.py
```

### Linux/Mac vagy Virtual Environment-tel

```bash
# 1. Virtual Environment létrehozása
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Függőségek telepítése
pip install -r requirements.txt

# 3. Futtatás
streamlit run app.py
```

---

## 📸 Használat

### 1. Adatok előkészítése
Helyezd el a képeket a `data/people/` mappába, személyenként külön almappákban:
```
data/people/
├── Person_A/
│   ├── foto1.jpg
│   └── foto2.jpg
└── Person_B/
    └── foto1.jpg
```

### 2. Database építés
- Az app automatikusan betölti a képeket indításkor
- Vagy kattints a **"🔄 Rebuild Database"** gombra a sidebaron

### 3. Arc felismerés
- Tölts fel egy képet az app-ban
- Az app megpróbálja felismerni az arcokat

---

## 📁 Projekt Struktúra
```
FaceRecognitionApp/
├── .streamlit/
│   └── config.toml        # Streamlit konfiguráció
├── src/                    # Forráskód modulok
│   ├── data_manager.py    # Arc adatbázis kezelő
│   ├── face_engine.py     # Arc felismerő engine
│   └── utils.py           # Segédfüggvények
├── data/                   # Lokális adattároló
│   ├── people/            # Személy mappák (gitignore!)
│   ├── encodings/         # Cache fájlok
│   └── logs/              # Log fájlok
├── config.py              # Központi konfiguráció
├── app.py                 # Alkalmazás belépési pont
├── requirements.txt       # Python függőségek
├── packages.txt           # Linux rendszer csomagok (Streamlit Cloud)
└── .gitignore            # Git kizárások
```

---

## 🛠️ Fejlesztés

### Code Quality
```bash
# Formázás
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

## ⚠️ Fontos megjegyzések

### GDPR & Privacy
- **A `data/people/` mappa .gitignore-ban van!**
- Soha ne commitolj személyes arcképeket
- Csak a saját gépeden tárold az éles képeket

### Streamlit Cloud Limitációk
- **Ingyenes tier:** 1 GB RAM, 1 CPU
- **Timeout:** 10 perc inaktivitás után alvó módba
- **Nem ajánlott:** Nagy adatbázisokhoz (>100 személy)

---

## 📄 Licensz
MIT License - Tanulási célú projekt

## 🤝 Kontribúció
Pull requestek és issue-k szívesen fogadva!
