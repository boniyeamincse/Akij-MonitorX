#!/bin/bash

# Update the OS
echo "Updating OS..."
sudo apt-get update && sudo apt-get upgrade -y

# Install prerequisites
echo "Installing prerequisites..."
sudo apt-get install -y \
    docker.io \
    docker-compose \
    git \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    curl \
    wget \
    nodejs \
    npm

# Setup Docker
echo "Setting up Docker..."
sudo systemctl start docker
sudo systemctl enable docker

# Create docker user if not exists
if ! id -u dockeruser &>/dev/null; then
    echo "Creating dockeruser..."
    sudo useradd -m -s /bin/bash dockeruser
    sudo usermod -aG docker dockeruser
    echo "dockeruser created with password 'dockerpass'. Change it after first login."
    echo 'dockeruser:dockerpass' | sudo chpasswd
fi

sudo usermod -aG docker $USER

# Install Docker Compose if not installed via apt
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Verify installations
echo "Verifying installations..."
docker --version
docker-compose --version
python3 --version
pip3 --version
node --version
npm --version
git --version

echo "Installation complete!"
echo ""
echo "Needed user credentials and setup:"
echo "- Zabbix Web: http://localhost:8080 (Admin/zabbix)"
echo "- Grafana: http://localhost:3000 (admin/admin)"
echo "- Alert Manager: http://localhost:9093"
echo ""
echo "Configure .env file with SMTP credentials for email notifications:"
echo "- SMTP_SERVER=smtp.gmail.com"
echo "- SMTP_PORT=587"
echo "- SMTP_USER=your-email@gmail.com"
echo "- SMTP_PASS=your-app-password (use Gmail app password)"
echo "- EMAIL_RECIPIENTS=admin@akij.com,manager@akij.com"
echo ""
echo "To run the project:"
echo "1. Copy .env.example to .env and fill in values"
echo "2. docker-compose up -d"
echo ""
echo "Note: Log out and back in for Docker group changes to take effect."