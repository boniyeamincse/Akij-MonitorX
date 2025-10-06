# Akij MonitorX Project Overview

## About the Project

Akij MonitorX is a comprehensive monitoring and analytics platform designed for Akij Group to monitor their IT infrastructure, detect anomalies using AI, and provide intelligent reporting. The system integrates multiple components including Zabbix for core monitoring, Grafana for visualization, AI-powered anomaly detection, and chatbot interfaces for natural language queries.

## Project Structure

### Root Directory Files
- `README.md` - Main project documentation with setup and usage instructions
- `package.json` - Node.js project configuration and scripts
- `docker-compose.yml` - Docker Compose configuration for full-stack deployment
- `docker-compose-plan.md` - Planning document for Docker Compose setup
- `.env` - Environment variables for local development
- `.env.example` - Example environment configuration
- `alertmanager.yml` - Alert Manager configuration for notifications

### Source Code (`src/`)
- `server.js` - Main Node.js Express server handling API endpoints and dashboard
- `agent.js` - Monitoring agent that collects system metrics and sends to server

### AI Engine (`ai-engine/`)
- `ai_engine.py` - Core AI engine with anomaly detection, forecasting, and reporting
- `chatbot.py` - Command-line chatbot interface
- `chatbot_api.py` - REST API for chatbot functionality
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration for AI engine container

### Documentation (`docs/`)
- `architecture.md` - System architecture overview
- `agentinstallationguide.md` - Agent deployment instructions
- `userguide.md` - User interface and operation guide
- `test.md` - Testing procedures and smoke tests
- `UNDERSTANDING.md` - Developer guide and understanding
- `DOCUMENTATION_EDIT_PLAN.md` - Documentation maintenance plan
- `docker-troubleshooting-cheatsheet.md` - Docker troubleshooting guide

### Web Assets (`public/`)
- `index.html` - Main dashboard HTML interface

### Grafana Configuration (`grafana/provisioning/`)
- `datasources/zabbix.yaml` - Grafana datasource configuration for Zabbix integration

## Key Features

### 1. Real-Time Monitoring
- CPU, RAM, Disk, Network, and Database metrics collection
- Zabbix agent integration for comprehensive system monitoring
- Custom service monitoring for Nginx, MySQL, Redis, etc.

### 2. AI-Powered Anomaly Detection
- **Isolation Forest**: Unsupervised anomaly detection
- **LSTM Autoencoder**: Deep learning for time-series anomaly detection
- **Prophet**: Trend forecasting and prediction

### 3. Predictive Analytics
- CPU/RAM usage forecasting
- System failure risk assessment
- Resource exhaustion prediction

### 4. Intelligent Alert Management
- AI-based alert prioritization (Critical, Warning, Low)
- Alert fatigue reduction through smart filtering
- Automated notification routing

### 5. Root Cause Analysis
- Correlation analysis between metrics
- Automated problem diagnosis
- Historical pattern analysis

### 6. Smart Reporting
- Automated PDF reports with anomaly highlights
- Daily/weekly performance summaries
- Email and scheduled report delivery

### 7. Chatbot Integration
- Natural language queries ("Show me CPU for Server-01")
- CLI and REST API interfaces
- Integration with monitoring data

## Technology Stack

### Backend
- **Node.js**: Server and agent implementation
- **Python**: AI engine and chatbot
- **Express.js**: REST API framework
- **Socket.IO**: Real-time communication

### Monitoring Infrastructure
- **Zabbix**: Core monitoring platform
- **Grafana**: Visualization and dashboards
- **Alert Manager (Prometheus)**: Alert management
- **MariaDB**: Database for Zabbix

### AI/ML Components
- **TensorFlow/Keras**: Deep learning models (LSTM)
- **Scikit-learn**: Traditional ML algorithms
- **Prophet**: Time-series forecasting
- **Transformers**: NLP for chatbot
- **NLTK**: Natural language processing

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Zabbix Agents │────│   Zabbix Server │────│   Grafana UI    │
│   (on Servers)  │    │   (Metrics DB)  │    │   (Dashboard)   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         v                       v                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Engine     │    │   Alert Manager │    │   Chatbot API   │
│   (Anomaly Det.)│    │   (Prometheus)  │    │   (NLP Queries) │
│   - LSTM,Prophet│    │   - Email/Slack │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start Guide

### Prerequisites
- Docker and Docker Compose
- Node.js 14+ (for development)
- Python 3.8+ (for AI components)

### Installation
1. Clone the repository
2. Run `npm install` for Node dependencies
3. Copy `.env.example` to `.env` and configure
4. Run `docker-compose up -d` for full deployment

### Access Points
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Zabbix Web**: http://localhost:8080 (Admin/zabbix)
- **Alert Manager**: http://localhost:9093
- **Node Server**: http://localhost:3000

## Development Workflow

### Local Development
1. Start Node server: `npm start`
2. Start agent: `npm run agent` (separate terminal)
3. Access dashboard at http://localhost:3000

### AI Engine Development
1. Create Python virtual environment
2. Install dependencies: `pip install -r ai-engine/requirements.txt`
3. Run AI engine: `python ai-engine/ai_engine.py`

### Docker Development
1. Build and start services: `docker-compose up --build`
2. View logs: `docker-compose logs -f`
3. Debug containers: `docker exec -it <container> /bin/bash`

## Configuration

### Environment Variables
Key configuration variables in `.env`:
- `ZABBIX_URL` - Zabbix API endpoint
- `ZABBIX_USER` - Zabbix username
- `ZABBIX_PASS` - Zabbix password
- `SMTP_*` - Email configuration
- `PORT` - Node server port

### Docker Compose Services
- `mariadb` - Database
- `zabbix-server-mysql` - Zabbix server
- `zabbix-web-nginx-mysql` - Zabbix web interface
- `zabbix-agent2` - Zabbix agent
- `ai-engine` - AI processing
- `alertmanager` - Alert management
- `grafana` - Visualization

## Testing

### Smoke Tests
- Node server + agent: `npm run smoke-test`
- Full stack: `docker-compose up -d` then verify services
- AI chatbot: Test API endpoints

### Automated Testing
- Unit tests for Node.js components
- Integration tests for API endpoints
- Container health checks

## Deployment Options

### 1. Docker Compose (Recommended)
```bash
docker-compose up -d
```

### 2. Individual Components
- Node server: `npm start`
- AI engine: `python ai-engine/ai_engine.py`
- Zabbix: Manual installation

### 3. Kubernetes
Future: Helm charts for Kubernetes deployment

## Troubleshooting

### Common Issues
- Port conflicts: Check if ports 3000, 8080, 9093 are available
- Docker permission denied: Add user to docker group
- AI engine fails: Check Python dependencies and Zabbix connectivity
- Database connection: Verify MariaDB container is running

### Logs and Debugging
- Application logs: `docker-compose logs`
- Node server logs: Console output from `npm start`
- AI engine logs: `docker logs ai-engine`

## Contributing

### Code Style
- Node.js: ESLint configuration
- Python: PEP 8 compliance
- Documentation: Markdown with consistent formatting

### Testing Requirements
- All new features must include tests
- Maintain >80% code coverage
- Pass all CI checks

## Security Considerations

### Authentication
- Zabbix: Default Admin/zabbix credentials (change in production)
- Grafana: Default admin/admin (change immediately)
- API endpoints: No authentication currently (add for production)

### Network Security
- Isolate containers with Docker networks
- Use HTTPS in production
- Restrict API access with firewalls

### Data Protection
- Encrypt sensitive configuration
- Secure database access
- Regular security updates

## Future Roadmap

### Planned Features
- Kubernetes deployment support
- Advanced AI models (GPT integration)
- Mobile dashboard app
- Multi-tenant architecture
- Advanced alerting rules

### Technical Improvements
- Microservices architecture
- GraphQL API
- Real-time streaming analytics
- Machine learning model versioning

## Support and Maintenance

### Documentation
- Comprehensive docs in `docs/` folder
- API documentation with examples
- Troubleshooting guides

### Monitoring
- Health check endpoints
- Performance monitoring
- Error tracking and alerting

### Backup and Recovery
- Database backups
- Configuration backups
- Disaster recovery procedures

## Contact Information

For support and questions:
- Documentation: Refer to `docs/` folder
- Issues: GitHub repository issues
- Email: support@akij.com (placeholder)

---

*This overview provides a comprehensive understanding of the Akij MonitorX project. For detailed implementation guides, refer to the specific documentation files in the `docs/` folder.*