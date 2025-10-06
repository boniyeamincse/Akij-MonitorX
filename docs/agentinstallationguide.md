# Agent Installation Guide for Akij MonitorX

## Prerequisites
- Linux/Windows/MacOS operating system
- Docker installed (if using containerized deployment)
- Network access to the central server
- Administrative privileges for installation

## Installation Steps

### Method 1: Docker Deployment (Recommended)
1. Pull the agent image:
   ```
   docker pull akij/monitorx-agent:latest
   ```

2. Run the container:
   ```
   docker run -d --name monitorx-agent \
     -e SERVER_URL=https://monitorx.akij.com \
     -e API_KEY=your-api-key \
     akij/monitorx-agent:latest
   ```

3. Verify installation:
   ```
   docker logs monitorx-agent
   ```

### Method 2: Binary Installation
1. Download the appropriate binary from the [releases page](https://github.com/akij/monitorx/releases).

2. Extract and install:
   ```
   tar -xzf monitorx-agent-v1.0.0-linux-amd64.tar.gz
   sudo mv monitorx-agent /usr/local/bin/
   ```

3. Create configuration file `/etc/monitorx/agent.conf`:
   ```
   server_url = "https://monitorx.akij.com"
   api_key = "your-api-key"
   ```

4. Start the service:
   ```
   sudo systemctl enable monitorx-agent
   sudo systemctl start monitorx-agent
   ```

### Method 3: Source Installation
1. Clone the repository:
   ```
   git clone https://github.com/akij/monitorx-agent.git
   cd monitorx-agent
   ```

2. Build the agent:
   ```
   go build -o monitorx-agent .
   ```

3. Configure and run as above.

## Configuration Options
- `server_url`: URL of the central monitoring server
- `api_key`: Authentication key for the server
- `interval`: Data collection interval (default: 30s)
- `log_level`: Logging verbosity (debug, info, warn, error)

## Troubleshooting
- Check agent logs for error messages.
- Verify network connectivity to the server.
- Ensure correct API key is configured.
- Restart the agent service if issues persist.

## Updates
To update the agent:
```
docker pull akij/monitorx-agent:latest
docker stop monitorx-agent
docker rm monitorx-agent
# Re-run the docker run command
```

For binary updates, download the new version and replace the binary.

## Support
If you encounter issues, check the [User Guide](userguide.md) or contact support.

## Simple installers (recommended for quick deploy)

This repository includes two convenience installer scripts to deploy the Node-based agent from the repo sources.

- Linux (Debian/Ubuntu): `scripts/agent-install.sh` — copies files to `/opt/akij-monitorx-agent` and creates a systemd service.
- Windows (PowerShell): `scripts/agent-install.ps1` — copies files to `%ProgramFiles%\AkijMonitorXAgent` and creates a Scheduled Task named `AkijMonitorXAgent` to run at startup.

Usage (Linux):

```bash
sudo bash scripts/agent-install.sh
```

Usage (Windows PowerShell as Administrator):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\\scripts\\agent-install.ps1
```

After installation check:

Linux:
```bash
systemctl status akij-monitorx-agent
journalctl -u akij-monitorx-agent -f
```

Windows (PowerShell):
```powershell
Get-ScheduledTask -TaskName AkijMonitorXAgent | Format-List *
# Logs depend on how the agent is configured; check the installed folder or agent log output
```