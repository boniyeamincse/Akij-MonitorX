# Docker Troubleshooting Cheatsheet

## Basic Commands
- Check Docker version: `docker --version`
- Check Docker Compose version: `docker-compose --version`
 - Start Docker service (Linux): `sudo systemctl start docker`
 - Enable Docker on boot (Linux): `sudo systemctl enable docker`
 - Check Docker status (Linux): `sudo systemctl status docker`
 - Windows notes: On Windows use Docker Desktop. Ensure WSL2 backend is enabled and Docker Desktop is running. There is no `systemctl` on Windows.

## Container Management
- List running containers: `docker ps`
- List all containers: `docker ps -a`
- Stop a container: `docker stop <container_name>`
- Remove a container: `docker rm <container_name>`
- View container logs: `docker logs <container_name>`
- Follow logs: `docker logs -f <container_name>`

## Image Management
- List images: `docker images`
- Remove image: `docker rmi <image_name>`
- Build image: `docker build -t <tag> .`
- Pull image: `docker pull <image>`

## Docker Compose
- Start services: `docker-compose up -d`
- Stop services: `docker-compose down`
- View logs: `docker-compose logs`
- Follow logs: `docker-compose logs -f`
- Rebuild and start: `docker-compose up --build -d`
- Scale service: `docker-compose up -d --scale <service>=<number>`

## Common Issues
- Permission denied: Add user to docker group: `sudo usermod -aG docker $USER` (logout/login required)
- Port already in use: `sudo lsof -i :port` to find, `sudo kill -9 <pid>` to kill
- No space left: `docker system prune -a` to clean up
- Container won't start: Check logs with `docker logs <container>`, validate environment variables
- Image pull fails: Check internet, or pull manually `docker pull <image>`
- Compose file invalid: `docker-compose config` to validate YAML

## Networking
- List networks: `docker network ls`
- Inspect network: `docker network inspect <network>`
- Connect container to network: `docker network connect <network> <container>`
- Disconnect: `docker network disconnect <network> <container>`

## Volumes
- List volumes: `docker volume ls`
- Remove volume: `docker volume rm <volume>`
- Inspect volume: `docker volume inspect <volume>`

## Debugging
- Enter running container: `docker exec -it <container> /bin/bash`
- Check container resource usage: `docker stats`
- Check system info: `docker system info`
- Clean up everything: `docker system prune -a --volumes`

## For This Project
- Start Akij MonitorX: `docker-compose up -d`
- Stop: `docker-compose down`
- Check Zabbix logs: `docker logs zabbix-server`
- Check AI Engine logs: `docker logs ai-engine`
- Access Zabbix: http://localhost:8080 (Admin/zabbix)
- Access Grafana: http://localhost:3000 (admin/admin)

Project tips:
- If you are on Windows, start Docker Desktop and enable WSL2 integration for your distro.
- Before running `docker-compose up`, ensure ports (3000, 8080, 9093, etc.) are free.
- Use the repository's smoke-test to verify Node server + agent: `npm run smoke-test` (PowerShell).
- For lightweight Python API testing, install minimal requirements in `ai_engine/requirements.txt`.