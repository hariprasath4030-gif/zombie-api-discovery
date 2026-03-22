# Zombie (Stale/Defunct) API Discovery and Defence

## 1) Full Architecture (Simple View)

```text
[Scanner] -> [API Analyzer] -> [Security Checker] -> [Dashboard]
                               |
                               v
                        [Alert / Fix System]
```

## 2) Technologies (Only 2)

- Python (Backend + Scanner)
- React (Frontend Dashboard)

## 3) Modules Implemented

1. API Discovery Module
   - Scans URLs
   - Scans Swagger/OpenAPI URLs
   - Parses local log files for endpoint patterns
2. API Analyzer Module
   - Classifies API status as active / deprecated / orphaned / zombie
3. Security Checker Module
   - Checks authentication, encryption, rate limiting, and data exposure indicators
4. Alert/Fix Module
   - Generates actionable alerts
   - Creates simulated automated fix queue items
5. Dashboard Module
   - Summary cards
   - API results table
   - Alerts and fix queue

## 4) Project Structure

```text
Zombie API project/
├─ .github/
│  └─ workflows/
│     └─ scheduled-scan.yml
├─ .gitignore
├─ README.md
├─ backend/
│  ├─ requirements.txt
│  ├─ run_scheduled_scan.py
│  ├─ package-lock.json
│  └─ app/
│     ├─ __init__.py
│     ├─ main.py
│     ├─ models.py
│     ├─ storage.py
│     ├─ data/
│     │  └─ sample_api_logs.txt
│     └─ modules/
│        ├─ __init__.py
│        ├─ discovery.py
│        ├─ analyzer.py
│        ├─ security.py
│        └─ alerts.py
├─ frontend/
│  ├─ package.json
│  ├─ package-lock.json
│  ├─ vite.config.js
│  ├─ index.html
│  └─ src/
│     ├─ main.jsx
│     ├─ App.jsx
│     ├─ index.css
│     ├─ api/
│     │  └─ client.js
│     └─ components/
│        ├─ SummaryCards.jsx
│        ├─ ApiTable.jsx
│        └─ AlertsPanel.jsx
```

## 5) Final Simple Plan (Step-by-Step)

### Step 1: Python -> Scan APIs

Backend endpoints used:
- `POST /api/discover`
- `GET /api/results`
- `GET /api/alerts`
- `POST /api/fix`
- `GET /api/report`

### Step 2: Store results (JSON/DB)

- Results are stored in:
  - `backend/app/data/api_results.json`

### Step 3: Apply rules -> classify

- Classification values:
  - `active`
  - `deprecated`
  - `orphaned`
  - `zombie`

### Step 4: React -> show dashboard

- Dashboard page in `frontend/src/App.jsx`

### Step 5: Add alerts

- Alerts from `GET /api/alerts`
- Automated fix queue from `POST /api/fix`

## 6) Terminal Commands (Run from project root)

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on `http://127.0.0.1:8000`

### Frontend (new terminal)

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on `http://127.0.0.1:5173`

## 7) Optional nmap

If you want infrastructure-level scan support later:

```powershell
nmap -sV <target-host>
```

This is optional and not required for current app flow.
