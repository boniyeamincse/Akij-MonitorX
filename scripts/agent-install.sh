#!/usr/bin/env bash
# Agent installer for Debian/Ubuntu
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "This installer requires sudo/root. Re-run with sudo." >&2
  exit 1
fi

PROJECT_DIR="/opt/akij-monitorx-agent"
echo "Installing Akij MonitorX agent to $PROJECT_DIR"

mkdir -p "$PROJECT_DIR"
cp -r ./* "$PROJECT_DIR/"

echo "Creating systemd service..."
cat >/etc/systemd/system/akij-monitorx-agent.service <<'SERVICE'
[Unit]
Description=Akij MonitorX Agent
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/node /opt/akij-monitorx-agent/src/agent.js
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable akij-monitorx-agent
systemctl start akij-monitorx-agent

echo "Agent installed and started. Check status with: systemctl status akij-monitorx-agent"
