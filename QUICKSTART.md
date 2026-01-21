# 🚀 GYORS INDÍTÁS - 2 PERC

## Windows Userek (A LEGEGYSZERŰBB):

### 1. Dupla klikk:
```
install_windows.bat
```

### 2. Futtasd:
```
streamlit run app.py
```

**Kész!** 🎉

---

## Ha a batch file nem működik:

### Terminálban (3 parancs):
```bash
pip install dlib-bin
pip install --no-deps face-recognition
pip install streamlit opencv-python numpy pillow face-recognition-models
```

### Futtasd:
```bash
streamlit run app.py
```

---

## Mac / Linux:

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📸 Tesztelés:

1. **Add hozzá képeket:**
   - Menj a `data/people/` mappába
   - Hozz létre egy mappát, pl: `data/people/Te/`
   - Tegyél bele 2-3 képet magadról (jpg/png)

2. **Indítsd újra az appot**
   - Ctrl+C a terminálban
   - `streamlit run app.py`

3. **Próbáld ki:**
   - Tölts fel egy képet magadról
   - Az app megpróbálja felismerni!

---

## ❓ Problémák?

### "dlib error" Windows-on:
```bash
pip uninstall dlib
pip install dlib-bin
```

### "Module not found":
```bash
pip install -r requirements-windows.txt --upgrade
```

### "Port már használatban":
```bash
streamlit run app.py --server.port 8502
```

---

## 🌐 Online verzió:

**Nem akarsz telepíteni?**  
Próbáld ki online: [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)

*Az online verzió üres adatbázissal indul (GDPR miatt nincs előre feltöltve kép).*
