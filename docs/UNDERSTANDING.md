UNDERSTANDING Akij MonitorX
==========================

Purpose
-------
This document explains the overall architecture, development workflow, how to run the application and components, important environment variables, common troubleshooting steps, and recommended next steps for contributors and operators.

Who this is for
----------------
- Developers who want to run and modify the server, agent, or AI modules.
- DevOps / operators who will deploy the stack (Docker Compose is the suggested approach).
- Anyone who needs a quick mental model of how the pieces fit together.

High-level architecture
-----------------------
Akij MonitorX is a lightweight monitoring platform which collects metrics from agents, stores and visualizes them (Zabbix/Grafana), and runs an AI engine for anomaly detection, prioritization and reporting. The repo contains three main components:

1. Node server and web UI (in `src/`) — Receives metrics from agents, serves the dashboard in `public/`, and emits real-time updates via Socket.IO.
2. Agent (in `src/agent.js`) — Simple Node script that collects OS metrics and posts them to the server.
3. AI Engine (in `ai_engine/`) — A Python package containing anomaly detection, forecasting, reporting and chatbot integration.

There are supporting artifacts for Docker Compose and docs at the project root.

Key files and directories
------------------------
- `package.json` — Node project metadata and npm scripts.
- `src/server.js` — Express + Socket.IO server that serves the dashboard and metrics API.
- `src/agent.js` — Simple agent that posts OS metrics to the server.
- `public/` — Static web UI (dashboard index.html is here).
- `ai_engine/` — Python package (anomaly detection, reporting, chatbot API). Use Python virtualenv to run.
- `docker-compose.yml` — Optional infrastructure orchestration (Zabbix, Grafana, etc.)
- `docs/` — Documentation and guides (this file is `UNDERSTANDING.md`).

Quick start (developer)
-----------------------
Prerequisites
- Node.js v14+ (or whichever your CI uses)
- npm
- Python 3.8+ (for AI components)
- Docker & Docker Compose (optional, recommended for full stack)

1. Install Node deps

```powershell
cd "d:\Akij Group\Akij MonitorX"
npm install
```

2. Start the Node server

```powershell
npm start
# or for development with auto-restart
npm run dev
```

3. Start an agent locally (another terminal)

```powershell
npm run agent
```

4. Open the dashboard in your browser

- http://localhost:3000

5. Run the Python chatbot API (optional)

Create and activate a virtual environment, then install minimal deps (Flask and zabbix_api or mocks):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install flask zabbix-api
python -m ai_engine.chatbot_api
```

Notes about Python AI engine
---------------------------
- The Python package lives in `ai_engine/`. It contains heavy ML dependencies (TensorFlow, Prophet, transformers) in the full implementation. For quick tests, you can install only the pieces you need (e.g., `flask`, `zabbix-api`) and mock the ML features.
- Running the AI engine end-to-end requires access to a Zabbix server (or mocking of `zabbix_api.ZabbixAPI`).
- The CLI chatbot and `chatbot_api` import functions from `ai_engine.ai_engine`.

Important environment variables
-------------------------------
Set these in a `.env` file in the project root or via your Docker Compose/host env.

Node server
- PORT — port for the Node server (default: 3000)

Agent
- SERVER_URL — URL for the Node server (default: http://localhost:3000)
- AGENT_ID — optional identifier for this agent
- INTERVAL — metrics interval in milliseconds (default: 30000)

Python AI (examples)
- ZABBIX_URL — Zabbix API endpoint (default: http://localhost:8080/api_jsonrpc.php)
- ZABBIX_USER — Zabbix username (default: Admin)
- ZABBIX_PASS — Zabbix password (default: zabbix)
- SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS — for email reports
- EMAIL_RECIPIENTS — CSV list of recipients

Troubleshooting & common issues
-------------------------------
1. Dashboard shows blank / 404
- Ensure the Node server is running from the project root and the `public` folder exists.
- Confirm `src/server.js` serves the project's `public/index.html` by using `http://localhost:3000/`.

2. Agent can't reach server
- Verify `SERVER_URL` env var and firewall rules.
- Run `npm run agent` locally and check console logs for failure messages.
- Use `curl` or Postman to POST to `http://localhost:3000/api/metrics` and confirm the server returns `{ status: 'ok' }`.

3. Python imports fail for AI Engine
- Ensure you're using `ai_engine` (underscore) as the package name. The project previously had `ai-engine` (hyphen) which is invalid for Python imports.
- Activate your virtualenv and install required packages.

4. Heavy Python deps failing to install
- TensorFlow, Prophet, and transformers are large and have OS-specific wheels. Prefer running these components inside Docker on a Linux host or use a server with the appropriate binaries.

5. Zabbix integration fails
- Confirm Zabbix API URL and credentials.
- Use a small script to `zapi = ZabbixAPI(ZABBIX_URL); zapi.login(user, pass)` to validate connectivity.

Developer tips / conventions
---------------------------
- Keep Node env vars in `.env`. Do not commit secrets.
- For small experiments, you can stub `zabbix_api` with a tiny local fake that returns predictable data.
- When changing static assets in `public/`, restart the server (or use `nodemon` / `npm run dev`).

Suggested next improvements (low-risk)
-------------------------------------
- Add a `requirements.txt` for `ai_engine/` separating minimal runtime deps (Flask, zabbix-api) from heavy ML deps (tensorflow, prophet, transformers).
- Add a Dockerfile for the `ai_engine` package with GPU/CPU variants and a matching service in `docker-compose.yml` for reproducible deployment.
- Add a small smoke test script that starts the Node server, runs the agent once, and checks `/api/metrics` for expected data.
- Add unit tests for core utilities in `ai_engine` and for the Node API endpoints (e.g., using Jest + supertest).

Where to find things to change
-----------------------------
- API: `src/server.js`
- Agent: `src/agent.js`
- Python AI: `ai_engine/` (functions: `chatbot_query`, `get_zabbix_api`)
- Docs: `docs/`, `README.md`, `docs/docker-troubleshooting-cheatsheet.md`

Contact & ownership
-------------------
If you have team contacts, add a `MAINTAINERS.md` or update README with owners and preferred contact channels for production incidents.

Done checklist for this doc
---------------------------
- [x] Architecture overview
- [x] How to run (Node + Agent)
- [x] How to run minimal Python API
- [x] Env vars list
- [x] Troubleshooting pointers
- [x] Next improvement suggestions

---

If you want, I can next:
- Add a minimal `ai_engine/requirements.txt` (minimal vs full) and a lightweight Dockerfile for the Python API.
- Create a smoke-test script and run it locally (start server + agent + check endpoint). 
- Update `docs/docker-troubleshooting-cheatsheet.md` to include Windows Docker notes.

Tell me which of the above to do next and I will proceed.  