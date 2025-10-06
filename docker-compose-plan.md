# Docker Compose Design for Zabbix Monitoring Stack with Grafana

## Overview
This docker-compose.yml sets up a basic monitoring stack including:
- Zabbix Server with PostgreSQL backend
- Zabbix Web interface (Nginx-based)
- Zabbix Agent for local monitoring
- Grafana for visualization and dashboards

## Architecture
```
[PostgreSQL] <-- [Zabbix Server] <-- [Zabbix Agent]
              <-- [Zabbix Web] <-- Browser (port 8080)
              <-- [Grafana] <-- Browser (port 3000)
```

All services communicate via a shared Docker network (`zabbix-net`).

## Services Configuration

### PostgreSQL
- **Image**: `postgres:13`
- **Purpose**: Database backend for Zabbix
- **Environment Variables**:
  - `POSTGRES_USER`: zabbix
  - `POSTGRES_PASSWORD`: zabbix
  - `POSTGRES_DB`: zabbix
- **Volumes**: `postgres_data:/var/lib/postgresql/data`
- **Network**: zabbix-net

### Zabbix Server
- **Image**: `zabbix/zabbix-server-pgsql:latest`
- **Purpose**: Core Zabbix server component
- **Environment Variables**:
  - `DB_SERVER_HOST`: postgres
  - `POSTGRES_USER`: zabbix
  - `POSTGRES_PASSWORD`: zabbix
  - `POSTGRES_DB`: zabbix
- **Ports**: `10051:10051` (server port)
- **Volumes**: `zabbix_server_data:/var/lib/zabbix`
- **Depends on**: postgres
- **Network**: zabbix-net

### Zabbix Web
- **Image**: `zabbix/zabbix-web-nginx-pgsql:latest`
- **Purpose**: Web interface for Zabbix
- **Environment Variables**:
  - `ZBX_SERVER_HOST`: zabbix-server
  - `DB_SERVER_HOST`: postgres
  - `POSTGRES_USER`: zabbix
  - `POSTGRES_PASSWORD`: zabbix
  - `POSTGRES_DB`: zabbix
- **Ports**: `8080:8080` (web interface)
- **Depends on**: postgres, zabbix-server
- **Network**: zabbix-net

### Zabbix Agent
- **Image**: `zabbix/zabbix-agent:latest`
- **Purpose**: Monitoring agent for the host/container
- **Environment Variables**:
  - `ZBX_SERVER_HOST`: zabbix-server
- **Ports**: `10050:10050` (agent port)
- **Network**: zabbix-net

### Grafana
- **Image**: `grafana/grafana:latest`
- **Purpose**: Visualization platform
- **Ports**: `3000:3000` (Grafana UI)
- **Volumes**: `grafana_data:/var/lib/grafana`
- **Network**: zabbix-net

## Volumes
- `postgres_data`: Persistent storage for PostgreSQL data
- `zabbix_server_data`: Persistent storage for Zabbix server data
- `grafana_data`: Persistent storage for Grafana data

## Networks
- `zabbix-net`: Isolated network for service communication

## Complete docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    container_name: zabbix-postgres
    environment:
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: zabbix
      POSTGRES_DB: zabbix
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - zabbix-net

  zabbix-server:
    image: zabbix/zabbix-server-pgsql:latest
    container_name: zabbix-server
    environment:
      DB_SERVER_HOST: postgres
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: zabbix
      POSTGRES_DB: zabbix
    ports:
      - "10051:10051"
    depends_on:
      - postgres
    volumes:
      - zabbix_server_data:/var/lib/zabbix
    networks:
      - zabbix-net

  zabbix-web:
    image: zabbix/zabbix-web-nginx-pgsql:latest
    container_name: zabbix-web
    environment:
      ZBX_SERVER_HOST: zabbix-server
      DB_SERVER_HOST: postgres
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: zabbix
      POSTGRES_DB: zabbix
    ports:
      - "8080:8080"
    depends_on:
      - postgres
      - zabbix-server
    networks:
      - zabbix-net

  zabbix-agent:
    image: zabbix/zabbix-agent:latest
    container_name: zabbix-agent
    environment:
      ZBX_SERVER_HOST: zabbix-server
    ports:
      - "10050:10050"
    networks:
      - zabbix-net

  grafana:
    image: grafana/grafana:latest
    container_name: zabbix-grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - zabbix-net

volumes:
  postgres_data:
  zabbix_server_data:
  grafana_data:

networks:
  zabbix-net:
    driver: bridge