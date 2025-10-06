#!/usr/bin/env bash
set -euo pipefail

# Production setup helper (Debian/Ubuntu)
# - Installs Node and docker if missing (best-effort)
# - Creates a dedicated service user
# - Installs agent to /opt/akij-monitorx-agent and configures systemd service under that user

if [ $(id -u) -ne 0 ]; then
  echo "Please run as root: sudo ./scripts/setup.sh" >&2
  exit 1
fi

APP_USER=akij
APP_DIR=/opt/akij-monitorx-agent

echo "Creating user $APP_USER (if missing)"
if ! id -u $APP_USER >/dev/null 2>&1; then
  useradd --system --create-home --shell /bin/false $APP_USER
fi

echo "Copying files to $APP_DIR"
mkdir -p $APP_DIR
rsync -a --exclude='.git' --exclude='node_modules' . $APP_DIR/
chown -R $APP_USER:$APP_USER $APP_DIR

echo "Creating systemd service for agent"
cat >/etc/systemd/system/akij-monitorx-agent.service <<EOF
[Unit]
Description=Akij MonitorX Agent
After=network.target

[Service]
Type=simple
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/env node $APP_DIR/src/agent.js
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable akij-monitorx-agent
systemctl start akij-monitorx-agent

echo "Agent service installed and started as $APP_USER. Check status: systemctl status akij-monitorx-agent"
