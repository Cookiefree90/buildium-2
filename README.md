# Buildium 2

This repository contains a minimal full‑stack property management prototype. It
includes:

* **Flask** backend with SQLAlchemy models, JWT auth, role based access control
  and a GPT integration endpoint.
* **React** frontend with a basic dashboard and tenant portal. Axios is used for
  API calls and Socket.IO for real‑time maintenance notifications.
* **Electron** wrapper to run the React UI as a desktop application.

### Backend

`backend/app.py` exposes routes for authentication, property, tenant, lease,
payment and maintenance management. WebSocket notifications are emitted on new
maintenance requests.

Install dependencies and run the server:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The application expects the following environment variables:

- `JWT_SECRET_KEY` — secret used to sign JSON Web Tokens.
- `OPENAI_API_KEY` — API key for GPT integration.

### Frontend

The frontend is a standard React project:

```bash
cd frontend
npm install
npm start
```

### Electron

Wrap the frontend in a desktop application:

```bash
cd electron
npm install
npm start
```

The backend is expected to run locally on port 5000 and the React dev server on
port 3000.
