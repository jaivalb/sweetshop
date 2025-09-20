# Sweet Shop — FastAPI + MongoDB + React (Vite)

This is a full‑stack CRUD app with authentication. Backend is FastAPI (JWT, Motor for MongoDB). Frontend is React + TypeScript (Vite) with a minimal UI.

GUI:
![Screenshot](frontend/gui-sample.png)

## Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (Docker Desktop or local install)

## Quick Start (Windows PowerShell)
```powershell
# 1) Clone and open the repo
cd D:\incuby

# 2) Create backend .env
@"
SECRET_KEY=dev-secret-change
ACCESS_TOKEN_EXPIRES_MINUTES=1440
MONGO_URI=mongodb://root:example@localhost:27017/?authSource=admin
MONGO_DB=sweetshop
"@ | Out-File -Encoding ascii backend/.env

# 3) (Option A) Start MongoDB with Docker
docker compose up -d
# or (Option B) Use a local MongoDB install and set MONGO_URI accordingly

# 4) Create venv and install backend deps
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\pip.exe install -r backend\requirements.txt

# 5) Run API
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --app-dir backend
# API: http://localhost:8000 (Docs: http://localhost:8000/docs)

# 6) In a second terminal, install and run frontend
cmd /c "cd frontend & npm install & npm run dev"
# Web: http://localhost:5173 (proxy to /api -> http://localhost:8000)
```

## From‑Scratch Implementation Guide

1. Initialize project structure
   - Create `backend/` and `frontend/` folders.
   - Backend packages: `fastapi`, `uvicorn[standard]`, `motor`, `pydantic-settings`, `python-jose[cryptography]`, `passlib[bcrypt]`, `email-validator`.
   - Frontend: `npm create vite@latest` (React + TS), add `react-router-dom`.

2. Backend setup
   - `app/main.py`: create `FastAPI`, add `CORSMiddleware` with `http://localhost:5173`, include routers.
   - `app/core/config.py`: load `SECRET_KEY`, `ACCESS_TOKEN_EXPIRES_MINUTES`, `MONGO_URI`, `MONGO_DB` from `backend/.env`.
   - `app/db/mongo.py`: create Motor client, `lifespan` with connectivity log, yield `AsyncIOMotorDatabase` via `get_db`.
   - `app/core/security.py`: implement `hash_password`, `verify_password`, `create_access_token` (HS256, `sub` + `exp`).
   - Models: `UserCreate`, `UserPublic`, `Token`, `LoginRequest`, `SweetCreate`, `SweetUpdate`.
   - Utils: `doc_to_public` converts `_id` to `id` and strips `hashed_password`.
   - Auth routes (`/api/auth`):
     - POST `/register` hashes password, inserts user, returns JWT.
     - POST `/login` verifies password, returns JWT.
     - GET `/me` returns `UserPublic` (no sensitive fields).
   - Deps: `get_current_user` decodes bearer token; `get_current_admin` checks `is_admin`.
   - Sweets routes (`/api/sweets`): CRUD, search, purchase/restock; admin guard where needed.

3. Frontend setup
   - `vite.config.ts` dev proxy `{ "/api": "http://localhost:8000" }`.
   - `src/auth/AuthContext.tsx`: store token in `localStorage`, fetch `/api/auth/me` with bearer token, expose `logout`.
   - `src/lib/api.ts`: helper that adds Authorization header when token exists.
   - Pages: `Login`, `Register`, `Dashboard` (listing, filters, purchase; admin actions add/edit/restock/delete).
   - Routing: `App.tsx` uses a `PrivateRoute` wrapper.
   - Styling: `src/styles.css` with container, cards, lists; imported in `src/main.tsx`.

4. CORS and proxy
   - Backend CORS allows `http://localhost:5173`.
   - Vite dev server proxies `/api` to `http://localhost:8000`.

## Common Issues & Fixes
- 401 on `/api/auth/me`: ensure Authorization header is `Bearer <token>` and backend `SECRET_KEY` is consistent.
- 400 on register/login: check Mongo is running and credentials match `MONGO_URI`.
- CORS errors: confirm origin `http://localhost:5173` is in `CORSMiddleware` allow list.

## Running Backend Tests
```powershell
# Ensure Mongo is running and backend venv is active
.\.venv\Scripts\python.exe -m pytest -q
```

## Production Notes
- Set strong `SECRET_KEY` and shorter token TTLs.
- Run Mongo with auth and a scoped DB user.
- Serve the built frontend (`npm run build`) behind a reverse proxy; run API with a production ASGI server (e.g., `uvicorn --workers 2` or `gunicorn -k uvicorn.workers.UvicornWorker`).

## API Overview
- `POST /api/auth/register` → `{ access_token }`
- `POST /api/auth/login` → `{ access_token }`
- `GET /api/auth/me` (Bearer) → user profile
- `GET /api/sweets` (Bearer) → list
- `GET /api/sweets/search` (Bearer) → filtered list
- `POST /api/sweets/` (Admin) → create
- `PUT /api/sweets/{id}` (Admin) → update price
- `DELETE /api/sweets/{id}` (Admin) → delete
- `POST /api/sweets/{id}/purchase?quantity=1` (Bearer)
- `POST /api/sweets/{id}/restock?quantity=5` (Admin)
