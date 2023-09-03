#!/usr/bin/env python3
import os
import subprocess
import requests
import logging

# Configure the logging settings
logging.basicConfig(filename='installation.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to execute shell commands and log the output
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logging.info(f'Success: {command}')
        else:
            logging.error(f'Error ({result.returncode}): {command}\n{result.stderr}')
    except Exception as e:
        logging.error(f'Exception: {e}')

# Modified run_command function
def run_command_with_input(command, input_text=None):
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if input_text:
            # Send "y" as input
            process.stdin.write(input_text)
            process.stdin.flush()

        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr

    except Exception as e:
        logging.error(f'Exception: {e}')
        return 1, '', str(e)

# Step 1: Download Docker installation script
logging.info('Step 1: Downloading Docker installation script')
try:
    script_url = 'https://get.docker.com'
    response = requests.get(script_url)
    if response.status_code == 200:
        with open('install-docker.sh', 'w') as f:
            f.write(response.text)
        logging.info('Download successful')
    else:
        logging.error(f'Failed to download script (HTTP {response.status_code})')
except Exception as e:
    logging.error(f'Exception while downloading script: {e}')

# Step 2: Set execute permissions on the downloaded script
logging.info('Step 2: Setting execute permissions')
try:
    os.chmod('install-docker.sh', 0o755)
    logging.info('Execute permissions set')
except Exception as e:
    logging.error(f'Exception while setting execute permissions: {e}')

# Step 3: Remove Snap packages
logging.info('Step 3: Removing Snap packages')
run_command('snap remove lxd')
run_command('snap remove core20')
run_command('snap remove snapd')

# Step 4: Disable Snapd services
logging.info('Step 4: Disabling Snapd services')
run_command('systemctl disable snapd.service')
run_command('systemctl disable snapd.socket')
run_command('systemctl stop snapd.service')

# Step 5: Disable Snapd seeded service
logging.info('Step 5: Disabling Snapd seeded service')
run_command('systemctl disable snapd.seeded.service')
run_command('systemctl stop snapd.seeded.service')

# Step 6: Remove Snapd cache
logging.info('Step 6: Removing Snapd cache')
run_command('rm -rf /var/cache/snapd/')

# Step 7: Autoremove Snapd (purge)
logging.info('Step 7: Autoremoving Snapd')
run_command('apt autoremove --purge snapd')

# Step 8: Remove Snap user directory
logging.info('Step 8: Removing Snap user directory')
run_command('rm -rf ~/snap')


# Step 9: Execute the Docker installation script
logging.info('Step 9: Running Docker installation script')
run_command('./install-docker.sh')

# Step 10: Configure the firewall and usermod
logging.info('Step 10: Configuring firewall and usermod')
run_command('usermod -aG docker chris')
run_command('ufw default deny incoming')
run_command('ufw default deny outgoing')
run_command('ufw default deny routed')
run_command('ufw allow from 104.28.195.1')
run_command('ufw allow from 104.28.227.1')

# run command "ufw enable" 
return_code, stdout, stderr = run_command_with_input('ufw enable', 'y\n')

if return_code == 0:
    logging.info('UFW enabled successfully')
else:
    logging.error(f'Error enabling UFW: {stderr}')

# Step 11: Remove packages
logging.info('Step 11: Removing packages')
run_command('apt remove -y telnet pastebinit netcat')

# Step 12: Run apt autoremove and reboot
logging.info('Step 12: Running apt autoremove')
#run_command('apt autoremove -y')
return_code, stdout, stderr = run_command_with_input('apt autoremove', 'y\n')

if return_code == 0:
    logging.info('APT Autoremove completed successfully')
else:
    logging.error(f'Error running apt autoremove: {stderr}')

logging.info('Step 13: Rebooting the system')
run_command('reboot')
