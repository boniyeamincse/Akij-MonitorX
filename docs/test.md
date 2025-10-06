Akij MonitorX — Testing Guide
=============================

This document helps testers and users verify the project works end-to-end on a development machine running Windows (PowerShell). It provides quick smoke tests for the Node server, the agent, and (optionally) the Python chatbot API and Docker Compose stack.

Quick checklist
---------------
- [ ] Node.js and npm installed
- [ ] Python 3 installed (for optional AI/chatbot tests)
- [ ] Docker & Docker Compose installed (optional for full-stack tests)

Smoke test 1 — Node server + agent (fast)
----------------------------------------
1. Open PowerShell (Windows) or a bash shell (Debian/Ubuntu) and go to project root:

PowerShell:

```powershell
cd "d:\Akij Group\Akij MonitorX"
```

Bash (Debian/Ubuntu):

```bash
cd /path/to/Akij\ MonitorX  # adjust path; if cloned to /home/user/Akij-MonitorX use that
```

2. Install Node dependencies (if not already installed):

```powershell
npm install
```

3. Start the Node server in one terminal:

```powershell
npm start
```

In bash you can also run:

```bash
npm start &
# or use the npm script for linux smoke test
npm run smoke-test:linux
```

Expected: Server logs showing "Akij MonitorX server running on port 3000" or your configured `PORT` value.

4. In another terminal start the agent to send metrics:

```powershell
npm run agent
```

Expected: Agent console logs showing "Metrics sent from <AGENT_ID>" every interval (default 30s). The server terminal should log receipt of metrics.

5. Verify metrics endpoint manually (after agent sent at least one batch):

```powershell
# Use curl (Windows 10+), or PowerShell Invoke-RestMethod
Invoke-RestMethod -Uri http://localhost:3000/api/metrics -Method GET
```

Expected: JSON output containing the agentId and metric data.

Smoke test 2 — Open dashboard
----------------------------
Open a browser and go to:

- http://localhost:3000/

Expected: The dashboard UI loads (public/index.html). If the page is blank, check server logs and `public/index.html` existence.

Smoke test 3 — Docker Compose full stack (optional)
---------------------------------------------------
This runs Zabbix, Grafana, AI engine, and other services as defined in `docker-compose.yml`.

1. From the project root run:

```powershell
docker-compose up -d
```

2. Wait a few minutes for services to start. Check container statuses:

```powershell
docker-compose ps
```

3. Check logs for a specific service, e.g., Zabbix server:

```powershell
docker-compose logs -f zabbix-server
```

Expected: Zabbix and Grafana services start without fatal errors. Access the services at the addresses in README (e.g., Zabbix at http://localhost:8080).

Smoke test 4 — Chatbot API (optional, Python)
-------------------------------------------
1. Create and activate a virtual environment and install minimal deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install flask zabbix-api
```

2. Start the chatbot API (in the activated venv):

```powershell
python -m ai_engine.chatbot_api
```

3. Test the `/query` endpoint with a simple payload (use Postman or curl):

```powershell
# Example using PowerShell Invoke-RestMethod - replace "Server-01" with an actual host name in your Zabbix
Invoke-RestMethod -Uri http://localhost:5000/query -Method POST -ContentType 'application/json' -Body '{"query":"cpu","host":"Server-01"}'
```

Expected: JSON response with `response` text or an error indicating the host wasn't found.

Troubleshooting
---------------
- Port conflicts: If a port is already in use, change `PORT` in `.env` (for Node) or the compose file, then restart.
- Agent not sending: Check `SERVER_URL` in env and agent logs. Use `Invoke-RestMethod` to POST to `/api/metrics` to test server response.
- Docker issues on Windows: Ensure Docker Desktop WSL2 backend is running. Use `docker system info` to validate.
- Python packages fail to install: Some ML packages are large; for quick API tests avoid installing TensorFlow / Prophet; just install `flask` and `zabbix-api`.

Automated test script (optional)
--------------------------------
The repository already includes two automated smoke-test scripts:

- Windows PowerShell: `scripts/smoke-test.ps1` — run with `npm run smoke-test`.
- Linux (Debian/Ubuntu) bash: `scripts/smoke-test.sh` — run with `npm run smoke-test:linux`.

These scripts start the server and agent, check `/api/metrics`, and clean up processes. Use them as a quick verification step after `npm install`.
