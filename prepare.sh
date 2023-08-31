#!/bin/bash

# Run apt update && apt upgrade in the background and suppress output
apt update > /dev/null 2>&1 && apt upgrade -y > /dev/null 2>&1 &

# Prepare Docker Compose directories
mkdir -p compose/{postgresql,mysql,mongodb,apache,nginx,redis}

# Create docker-compose.yml files in each directory
touch compose/postgresql/docker-compose.yml
touch compose/mysql/docker-compose.yml
touch compose/mongodb/docker-compose.yml
touch compose/apache/docker-compose.yml
touch compose/nginx/docker-compose.yml
touch compose/redis/docker-compose.yml

# Wait for the background job to finish (the apt update && apt upgrade)
wait

# Print success message
echo "OK, INITIAL PREPARATION DONE"

# Invoke Python script for further installation
echo "Running Python installation script..."
python3 setup.py