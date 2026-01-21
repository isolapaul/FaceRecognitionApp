# 🚀 QUICK START - 2 MINUTES

## Windows Users (THE EASIEST):

### 1. Double-click:
```
install_windows.bat
```

### 2. Run:
```
python -m streamlit run app.py
```

**Done!** 🎉

---

## If the batch file doesn't work:

### In Terminal (3 commands):
```bash
python -m pip install dlib-bin
python -m pip install --no-deps face-recognition
python -m pip install streamlit opencv-python numpy pillow face-recognition-models
```

### Run:
```bash
python -m streamlit run app.py
```

**Note:** If `streamlit` command doesn't work, always use `python -m streamlit`

---

## Mac / Linux:

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📸 Testing:

1. **Add images:**
   - Go to `data/people/` folder
   - Create a folder, e.g.: `data/people/John/`
   - Put 2-3 photos of yourself (jpg/png)

2. **Restart the app**
   - Ctrl+C in terminal
   - `python -m streamlit run app.py`

3. **Try it:**
   - Upload a photo of yourself
   - The app will try to recognize you!

---

## ❓ Troubleshooting

### "dlib error" on Windows:
```bash
python -m pip uninstall dlib
python -m pip install dlib-bin
```

### "Module not found":
```bash
python -m pip install -r requirements-windows.txt --upgrade
```

### "Port already in use":
```bash
python -m streamlit run app.py --server.port 8502
```

---

## 🌐 Online Version:

**Don't want to install locally?**  
Try it online: [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)

*The online version starts with an empty database (no pre-loaded images for GDPR compliance).*
