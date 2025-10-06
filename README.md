# Akij MonitorX

A comprehensive monitoring system for Akij Group services, providing real-time insights and alerting capabilities.

## 🧰 Features & Capabilities

🔎 1. Real-Time Monitoring

Collect CPU, RAM, Disk, Network, Database metrics from all servers using Zabbix agents.

Monitor running services (Nginx, MySQL, Redis, etc.).

🤖 2. AI-Based Anomaly Detection

AI detects unusual spikes, downtimes, or abnormal process behavior.

Uses historical Zabbix time-series data.

Model types:

Isolation Forest

LSTM Autoencoder

Prophet (for trend forecasting)

🧮 3. Predictive Analytics

Predicts future CPU/RAM load or storage exhaustion.

# Akij MonitorX

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Lightweight monitoring for infrastructure and services. Collects metrics from agents, provides a web dashboard, and includes an AI engine for anomaly detection, alert prioritization and reporting.

## Contents
- Features
- Quick start (Debian/Ubuntu)
- Quick start (Windows)
- Project layout
- Testing and smoke tests
- AI Engine notes
- Docker Compose
- Development workflow
- Contributing

---

## Features
- Real-time metrics collection (agents → Node server)
- Web dashboard (`public/`) with Socket.IO updates
- Simple agent (`src/agent.js`) for OS metrics
- AI Engine (`ai_engine/`) with anomaly detection, forecasting, reporting and chatbot API
- Docker Compose for full-stack deployment (Zabbix, Grafana, AI Engine)

## Quick start (Debian/Ubuntu)
1. Install prerequisites:

```bash
sudo apt update
sudo apt install -y nodejs npm git curl
# Docker: follow Docker docs for Ubuntu installation
```

2. Clone and install:

```bash
git clone https://github.com/boniyeamincse/Akij-MonitorX.git
cd Akij-MonitorX
npm install
```

3. Start server & agent:

```bash
npm start &
npm run agent
```

4. Quick verification (Linux):

```bash
npm run smoke-test:linux
```

## Quick start (Windows - PowerShell)
1. Install Node.js and Git for Windows.
2. Clone and install:

```powershell
git clone https://github.com/boniyeamincse/Akij-MonitorX.git
cd "Akij MonitorX"
npm install
```

3. Start server and agent:

```powershell
npm start
# in another terminal
npm run agent
```

4. Quick verification (PowerShell):

```powershell
npm run smoke-test
```

## Project layout
- `src/` — Node server and agent
- `public/` — Frontend / dashboard
- `ai_engine/` — Python AI package (chatbot API, analytics)
- `docs/` — Documentation and guides
- `scripts/` — smoke-test scripts

## Documentation
Primary docs are in the `docs/` folder. Quick links:

- `docs/UNDERSTANDING.md` — Project overview and developer guidance
- `docs/test.md` — Tester guide and smoke-test instructions (PowerShell & Bash)
- `docs/agentinstallationguide.md` — Agent installation and installers (Linux/Windows)
- `docs/docker-troubleshooting-cheatsheet.md` — Docker troubleshooting tips
- `docs/architecture.md` — Architecture reference
- `docs/userguide.md` — End-user guide

## Testing & smoke tests
- Windows: `npm run smoke-test` runs `scripts/smoke-test.ps1` (PowerShell)
- Linux: `npm run smoke-test:linux` runs `scripts/smoke-test.sh` (Debian/Ubuntu)
- Manual test steps and debugging: see `docs/test.md`

## AI Engine (Python) notes
- Minimal requirements: `ai_engine/requirements.txt` (Flask + zabbix-api)
- Heavy ML packages (TensorFlow, Prophet, transformers) are optional and best installed on Linux or in Docker.
- Use `python -m ai_engine.chatbot_api` to run the chatbot API after installing dependencies.

## Docker Compose (full stack)
- Run `docker-compose up -d` to start Zabbix, Grafana, and other services.
- On Ubuntu/Debian use Docker Engine; on Windows use Docker Desktop with WSL2.

## Development workflow
- Use `npm run dev` (nodemon) for development auto-reloads.
- Keep secrets out of git; use `.env` and never commit credentials.
- Add unit tests: I can add Jest + supertest for Node endpoints and a basic Python import test for CI.

## Contributing
- Open issues for bugs and feature requests.
- Send PRs against `main`. Small, focused PRs with tests are preferred.

---

If you want I can next:
- Add a `.gitignore` and commit it for you (recommended).
- Create a GitHub Actions workflow that runs smoke tests on push.
- Add unit tests and a CI setup.

Tell me which to do next and I'll continue.
- Zabbix Web Interface
- Zabbix Agent2 for monitoring
- AI Engine for anomaly detection
- Grafana with Zabbix integration
- Alert Manager for notifications (email, Telegram, Slack)

Access:
- Zabbix Web: http://localhost:8080 (Admin/zabbix)
- Grafana: http://localhost:3000 (admin/admin)
- Alert Manager: http://localhost:9093

## Contributing
Please refer to the documentation for development guidelines.

## License
[Specify License Here]