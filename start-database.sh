#!/usr/bin/env bash
# Use this script to start a docker container for a local development database

# TO RUN ON WINDOWS:
# 1. Install WSL (Windows Subsystem for Linux) - https://learn.microsoft.com/en-us/windows/wsl/install
# 2. Install Docker Desktop for Windows - https://docs.docker.com/docker-for-windows/install/
# 3. Open WSL - `wsl`
# 4. Run this script - `./start-database.sh`

# On Linux and macOS you can run this script directly - `./start-database.sh`

# .env file
# DJANGO_DB_NAME=django
# DJANGO_DB_USER=django
# DJANGO_DB_PASSWORD=password
# DJANGO_DB_HOST=localhost
# DJANGO_DB_PORT=5432

DB_CONTAINER_NAME="news-scheduler-db"


if ! [ -x "$(command -v docker)" ] && ! [ -x "$(command -v podman)" ]; then
  echo -e "Docker or Podman is not installed. Please install docker or podman and try again.\nDocker install guide: https://docs.docker.com/engine/install/\nPodman install guide: https://podman.io/getting-started/installation"
  exit 1
fi

# determine which docker command to use
if [ -x "$(command -v podman)" ]; then
  DOCKER_CMD="podman"
elif [ -x "$(command -v docker)" ]; then
  DOCKER_CMD="docker"
fi

if ! $DOCKER_CMD info > /dev/null 2>&1; then
  echo "$DOCKER_CMD daemon is not running. Please start $DOCKER_CMD and try again."
  exit 1
fi

if command -v nc >/dev/null 2>&1; then
  if nc -z localhost "$DJANGO_DB_PORT" 2>/dev/null; then
    echo "Port $DJANGO_DB_PORT is already in use."
    exit 1
  fi
else
  echo "Warning: Unable to check if port $DJANGO_DB_PORT is already in use (netcat not installed)"
  read -p "Do you want to continue anyway? [y/N]: " -r REPLY
  if ! [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborting."
    exit 1
  fi
fi

if [ "$($DOCKER_CMD ps -q -f name=$DB_CONTAINER_NAME)" ]; then
  echo "Database container '$DB_CONTAINER_NAME' already running"
  exit 0
fi

if [ "$($DOCKER_CMD ps -q -a -f name=$DB_CONTAINER_NAME)" ]; then
  docker start "$DB_CONTAINER_NAME"
  echo "Existing database container '$DB_CONTAINER_NAME' started"
  exit 0
fi

# import env variables from .env
set -a
source .env


if [ "$DJANGO_DB_PASSWORD" = "password" ]; then
  echo "You are using the default database password"
  read -p "Should we generate a random password for you? [y/N]: " -r REPLY
  if ! [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Please set a password in the .env file and try again"
    exit 1
  fi
  # Generate a random URL-safe password
  DJANGO_DB_PASSWORD=$(openssl rand -base64 12 | tr '+/' '-_')
  sed -i "s/=password/=$DJANGO_DB_PASSWORD/g" .env
fi

$DOCKER_CMD run -d \
  --name $DJANGO_DB_NAME \
  -e POSTGRES_USER="$DJANGO_DB_USER" \
  -e POSTGRES_PASSWORD="$DJANGO_DB_PASSWORD" \
  -e POSTGRES_DB="$DJANGO_DB_NAME" \
  -p "$DJANGO_DB_PORT":5432 \
  docker.io/postgres && echo "Database container '$DB_CONTAINER_NAME' was successfully created"
