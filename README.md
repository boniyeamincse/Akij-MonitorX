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

Estimates system failure risk score per host.

⚙️ 4. Automated Alert Prioritization

AI classifies alerts as Critical, Warning, or Low Priority.

Reduces alert fatigue and false positives.

🧠 5. Intelligent Root Cause Analysis

AI correlates multiple metrics to find probable cause (e.g., high I/O + memory leak = DB issue).

🗄️ 6. Smart Reporting

Generates daily/weekly summaries of system performance.

Highlights anomalies and predictions in PDF or email.

🧩 7. Chatbot Integration (Optional)

Query system health using natural language:
"Hey AI, show me CPU for Server-01."

- CLI Chatbot: Run `python chatbot.py`
- API: Run `python chatbot_api.py` and POST to `/query` with {"query": "CPU", "host": "Server-01"}

## 🏗️ High-Level Architecture

```
+-------------------+     +-------------------+     +-------------------+
|   Zabbix Agents   |     |   Zabbix Server   |     |   Grafana UI      |
|   (on Servers)    |---->|   (Metrics DB)    |---->|   (Dashboard)     |
|   - CPU, RAM,     |     |   - MariaDB       |     +-------------------+
|   - Disk, Network |     |   - Zabbix Web    |
+-------------------+     +-------------------+     +-------------------+
          |                       |                       |
          |                       |                       |
          v                       v                       v
+-------------------+     +-------------------+     +-------------------+
|   AI Engine       |     |   Alert Manager   |     |   Chatbot API     |
|   (Anomaly Det.)  |     |   (Prometheus)    |     |   (NLP Queries)   |
|   - LSTM, Prophet |     |   - Email/Slack   |     +-------------------+
|   - Predictions   |     +-------------------+             |
+-------------------+             |                       |
          |                       |                       |
          v                       v                       v
+-------------------+     +-------------------+     +-------------------+
|   Smart Reports   |     |   Root Cause      |     |   Predictive      |
|   (PDF/Email)     |     |   Analysis        |     |   Analytics       |
+-------------------+     +-------------------+     +-------------------+
```

### Architecture Overview
- **Data Collection**: Zabbix agents collect metrics from monitored servers
- **Storage & Visualization**: Zabbix server stores data, Grafana provides dashboards
- **AI Processing**: AI Engine analyzes data for anomalies, predictions, and insights
- **Alerting & Notification**: Alert Manager handles prioritized alerts via multiple channels
- **Reporting**: Automated PDF reports with key insights
- **Interaction**: Optional chatbot for natural language system queries

## Use Case Examples
| Use Case | Description |
|----------|-------------|
| 🧩 Server Resource Monitoring | CPU, Memory, Disk, Load, Processes, and Uptime |
| ⚙️ Service Monitoring | Check Nginx, Apache, MySQL, SSH, or custom services |
| 🗄️ Database Monitoring | MySQL / PostgreSQL health, connection stats, slow queries |
| 🌐 Network Monitoring | Router and switch SNMP data, bandwidth usage |
| 🔔 Alert Management | Receive email or Telegram alerts for service downtime |
| 🧰 Performance Analysis | Graph historical performance data and trends |
| 🔒 Security Compliance | Detect unauthorized services or unexpected processes |
| 📈 Capacity Planning | Forecast resource needs using historical data |

## Installation
1. Install Node.js (version 14 or higher)
2. Clone the repository
3. Install dependencies:
   ```
   npm install
   ```
4. Copy `.env.example` to `.env` and configure environment variables

## Running the Application
- Start the server:
  ```
  npm start
  ```
- Start an agent (in a separate terminal):
  ```
  npm run agent
  ```

## Testing / Quick verification
- Run the built-in PowerShell smoke test (Windows):

```powershell
npm run smoke-test
```

- For manual testing see `docs/test.md` which contains PowerShell commands and Docker Compose checks.
- If you need to test the Python chatbot API quickly, install the minimal requirements in `ai_engine/requirements.txt` inside a virtualenv.
- Open http://localhost:3000 in your browser for the dashboard

## Quick Start
1. Review the [Architecture](docs/architecture.md) documentation
2. Follow the [Agent Installation Guide](docs/agentinstallationguide.md) to deploy agents
3. Refer to the [User Guide](docs/userguide.md) for detailed usage instructions

## Documentation
- [Architecture](docs/architecture.md)
- [User Guide](docs/userguide.md)
- [Agent Installation Guide](docs/agentinstallationguide.md)

## Deployment
Use Docker Compose for quick setup:
```
docker-compose up -d
```

The setup includes:
- Zabbix Server with MariaDB database
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