# 🚀 Deployment Guide - Streamlit Cloud

## Előfeltételek
- ✅ GitHub repository
- ✅ PostgreSQL adatbázis (ingyenes: Neon vagy Supabase)

---

## 1️⃣ PostgreSQL Adatbázis Létrehozása

### Opció A: Neon (Ajánlott)
1. Menj ide: https://neon.tech/
2. Regisztrálj ingyenes fiókkal
3. Hozz létre új projektet
4. Másold ki a **Connection String**-et (PostgreSQL URL formátumban)

### Opció B: Supabase
1. Menj ide: https://supabase.com/
2. Regisztrálj ingyenes fiókkal
3. Hozz létre új projektet
4. Settings → Database → Connection String → URI

**A Connection String így néz ki:**
```
postgresql://username:password@hostname:5432/database_name
```

---

## 2️⃣ GitHub Push

```bash
git add .
git commit -m "feat: multi-user authentication with PostgreSQL"
git push origin main
```

---

## 3️⃣ Streamlit Cloud Deployment

### Lépések:
1. **Menj ide:** https://share.streamlit.io/
2. **Bejelentkezés:** GitHub fiókkal
3. **New app** gomb
4. Válaszd ki a repository-t
5. **Main file:** `app.py`
6. **Python version:** 3.11 vagy újabb

### Advanced Settings:
7. Kattints **Advanced settings**
8. Add hozzá a **Secrets**:

```toml
DATABASE_URL = "postgresql://your_connection_string_here"
```

**FONTOS:** Cseréld le `your_connection_string_here`-t a Neon/Supabase-ből kapott URL-re!

9. **Deploy!** gomb

---

## 4️⃣ Első Használat

1. Az app betöltése után megjelenik a login képernyő
2. Kattints **Regisztráció**
3. Válassz felhasználónevet és jelszót
4. Lépj be
5. Töltsd fel az első képeket!

---

## 🔧 Troubleshooting

### "Database connection failed"
- ✅ Ellenőrizd, hogy a `DATABASE_URL` helyes-e a Secrets-ben
- ✅ Nézd meg a Neon/Supabase dashboardon, hogy aktív-e a DB
- ✅ Ellenőrizd, hogy nincs-e extra szóköz az URL-ben

### "Module not found"
- ✅ Ellenőrizd, hogy a `requirements.txt` tartalmazza az összes csomagot
- ✅ Redeploy az app-ot

### "Permission denied on data/users"
- ✅ Ez normális Streamlit Cloud-on! Az app automatikusan használja a PostgreSQL-t
- ✅ Helyi fájlrendszer nem használható production-ben

---

## 📊 User Isolation Működése

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

- ✅ **Passwords hashed:** bcrypt
- ✅ **PostgreSQL SSL:** automatic on Neon/Supabase
- ✅ **User isolation:** minden user külön mappa
- ✅ **No plaintext passwords:** soha!
- ✅ **GDPR compliant:** helyi tárolás vagy encrypted DB

---

## 🎉 Kész!

Az app most élőben fut és bárki elérheti akinek megadod az URL-t!

**App URL példa:**
```
https://your-username-face-recognition-app.streamlit.app
```

**Megosztás:**
- Küldd el az URL-t a felhasználóknak
- Ők regisztrálhatnak és használhatják
- Minden user izolált, saját adatbázist kap

---

## 🔄 Frissítés

Ha változtatsz a kódon:
```bash
git add .
git commit -m "update: ..."
git push
```

Streamlit Cloud **automatikusan** redeploy-ol! 🚀
