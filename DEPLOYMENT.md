# 🚀 Deployment Guide - Streamlit Cloud

## Előfeltételek
- GitHub repository
- PostgreSQL adatbázis

---

## 1️PostgreSQL Adatbázis Létrehozása

### Opció A: Neon (Ajánlott)
1. https://neon.tech/
2. Regisztrálj
3. Hozz létre új projektet
4. Másold ki a **Connection String**-et

### Opció B: Supabase
1. https://supabase.com/
2. Regisztrálj
3. Hozz létre új projektet
4. Settings → Database → Connection String → URI

## Streamlit Cloud Deployment

### Lépések:
1. https://share.streamlit.io/
3. **New app** gomb
4. Válaszd ki a repository-t
5. **Main file:** `app.py`
6. **Python version:** 3.11 vagy újabb
7. **Advanced settings**
8.  **Secrets**:

```toml
DATABASE_URL = "postgresql://your_connection_string_here"
```

9. **Deploy!**

---

## Első Használat

1. Az app betöltése után megjelenik a login képernyő
2. **Regisztráció**
3. Válassz felhasználónevet és jelszót
4. Lépj be
5. Töltsd fel az első képeket!

---

## 🔧 Troubleshooting

### "Database connection failed"
- Ellenőrizd, hogy a `DATABASE_URL` helyes-e a Secrets-ben
- Nézd meg a Neon/Supabase dashboardon, hogy aktív-e a DB

### "Module not found"
- Ellenőrizd, hogy a `requirements.txt` tartalmazza az összes csomagot
- Redeploy 


---

## User Isolation Működése

```
User 1:
  - Saját adatbázis mappa: data/users/user_1/
  - Saját face encodings: data/users/user_1/encodings/face_encodings.pkl
  
User 2:
  - Saját adatbázis mappa: data/users/user_2/
  - Saját face encodings: data/users/user_2/encodings/face_encodings.pkl
```

**Streamlit Cloud Limitation:**
- A fájlrendszer nem perzisztens!
- Ezért minden user saját mappában tárolja a face encodings-t
- PostgreSQL perzisztens: user adatok megmaradnak

---

## 🔐 Biztonsági Checklist

- **Passwords hashed:** bcrypt
- **PostgreSQL SSL:** automatic on Neon/Supabase
- **User isolation:** minden user külön mappa

---

## Kész!

Az app most élőben fut és bárki elérheti akinek megadod az URL-t!

**App URL példa:**
```
https://your-username-face-recognition-app.streamlit.app
```
