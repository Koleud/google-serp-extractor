# Google SERP Extractor

Webová aplikace pro extrakci přirozených (organických) výsledků vyhledávání z první strany Google pro zadané klíčové slovo s možností exportu do strojově čitelného formátu (JSON).

Vytvořeno jako praktický úkol pro společnost **INIZIO Internet Media** / **Collabim**.

---

## Funkce aplikace
- **Jeden vstupní parametr:** Přehledné webové rozhraní s jedním vstupním polem.
- **Čistá organika:** Automatická filtrace placených reklam (Google Ads), postranních panelů a nerelevantních prvků.
- **Export do JSON:** Možnost okamžitého stažení výsledků do souboru přímo v prohlížeči pomocí nativního Blob API.
- **Lokalizace pro ČR:** Dotazy jsou směrovány na český Google (`hl=cs`, `gl=cz`).
- **Stabilita a odolnost:** Řešení eliminuje pády způsobené consent obrazovkami GDPR a reCAPTCHA v3 na serveru.

---

## 🛠 Použité technologie
- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Data Provider:** SerpApi gateway
- **Testování:** Pytest
- **Kontejnerizace:** Docker, Docker Compose
- **Frontend:** Vanilla HTML/CSS/JavaScript (Fetch & Blob API)

---

## Rychlé spuštění lokálně

### 1. Klonování repozitáře
```bash
git clone https://github.com/Koleud/google-serp-extractor.git
cd google-serp-extractor
```

### 2. Příprava virtuálního prostředí
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalace závislostí
```powershell
pip install -r requirements.txt
```

### 4. Nastavení proměnných prostředí
V kořenovém adresáři vytvořte soubor `.env` s vaším API klíčem:
```env
SERPAPI_KEY=vas_api_klic
```

### 5. Spuštění serveru
```powershell
uvicorn main:app --reload
```
Aplikace poběží na adrese: `[http://127.0.0.1:8000](http://127.0.0.1:8000)`

---

## Unit testy

Testy jsou plně izolované a deterministické — nevyžadují připojení k internetu a nečerpají kvótu API (používají mockovaná data):

```powershell
pytest -v
```

Testovací scénáře pokrývají:
- Správné odfiltrování placené reklamy a zachování výhradně organických položek.
- Ignorování neúplných a prázdných výsledků.
- Korektní chování parseru při prázdném vstupním JSONu.

---

## Spuštění v Dockeru

Aplikaci lze spustit v izolovaném kontejneru jedním příkazem:

```powershell
docker compose up --build
```
Webové rozhraní bude dostupné na portu `8000`.

---
