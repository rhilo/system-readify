#!/bin/sh

#!/bin/bash

# Read environment variables from .env file
source .env

# Update and Upgrade Packages
update_upgrade() {
    apt update && apt upgrade -y
}

# Add User
add_user() {
    adduser --disabled-password --gecos "" $LOCALUSER
    echo "$LOCALUSER:$LOCALPASS" | chpasswd
    usermod -aG sudo $LOCALUSER
}

# Configure UFW
configure_ufw() {
    if [ "$ENABLEUFW" = "true" ]; then
        ufw enable
        IFS=',' read -ra ADDR <<< "$ALLOWEDIPV4"
        for i in "${ADDR[@]}"; do
            i=$(echo $i | xargs)
            ufw allow from "$i" to any port any
        done

        IFS=',' read -ra ADDR <<< "$ALLOWEDIPV6"
        for i in "${ADDR[@]}"; do
            i=$(echo $i | xargs)
            ufw allow from "$i" to any port any
        done
    fi
}

# Placeholder for installing packages
install_packages() {
    # Install Docker
    if [ "$DOCKER" = "true" ]; then
        echo "Installing Docker..."
    fi

    # Install Node.js
    if [ "$NODEJS" = "true" ]; then
        echo "Installing Node.js..."
    fi

    # Install PHP
    if [ "$PHP" = "true" ]; then
        echo "Installing PHP..."
    fi

    # Install Apache2
    if [ "$APACHE2" = "true" ]; then
        echo "Installing Apache2..."
    fi

    # Install Nginx
    if [ "$NGINX" = "true" ]; then
        echo "Installing Nginx..."
    fi

    # Install MySQL
    if [ "$MYSQL" = "true" ]; then
        echo "Installing MySQL..."
    fi

    # Install MongoDB
    if [ "$MONGODB" = "true" ]; then
        echo "Installing MongoDB..."
    fi

    # Install Redis
    if [ "$REDIS" = "true" ]; then
        echo "Installing Redis..."
    fi

    # Install PostgreSQL
    if [ "$POSTGRESQL" = "true" ]; then
        echo "Installing PostgreSQL..."
    fi
}


# Main function to call other functions
main() {
    update_upgrade
    add_user
    configure_ufw
    install_packages
}

# Execute main function
main
