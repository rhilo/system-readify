#!/usr/bin/env python3

import subprocess

# Function to execute and log a shell command
def execute_and_log(command, log_file):
    with open(log_file, 'a') as f:
        try:
            result = subprocess.run(command, stdout=f, stderr=f, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            f.write(f'An error occurred while executing: {command}\n')
            return False

log_file = 'status.log'

# Install prerequisites for Node.js
if execute_and_log("apt install -y ca-certificates curl gnupg", log_file):
    print("Prerequisites installed, proceeding...")

    # Create keyring directory
    execute_and_log("mkdir -p /etc/apt/keyrings", log_file)

    # Add NodeSource GPG key to the keyring
    execute_and_log("curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg", log_file)

    # Define NODE_MAJOR version from environment variable
    node_major = "20"

    # Add NodeSource to APT sources
    execute_and_log(f"echo 'deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_{node_major}.x nodistro main' | sudo tee /etc/apt/sources.list.d/nodesource.list", log_file)

else:
    print("Failed to install prerequisites, cannot proceed.")