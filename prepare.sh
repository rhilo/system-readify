#!/bin/bash

# Run apt update && apt upgrade in the background and suppress output
apt update > /dev/null 2>&1 && apt upgrade -y > /dev/null 2>&1 &

# Prepare Docker Compose directories one by one
echo "Creating compose directory..."
mkdir -p compose

echo "Creating service directories and files..."
for service in postgresql mysql mongodb apache nginx redis
do
    mkdir -p "compose/$service"
    touch "compose/$service/docker-compose.yml"
done

# Wait for the background job to finish (the apt update && apt upgrade)
wait

# Print success message
echo "OK, INITIAL PREPARATION DONE"

# Invoke Python script for further installation
echo "Running Python installation script..."
python3 setup.py