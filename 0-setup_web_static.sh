#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# Update system
sudo apt-get update -y

# Install nginx
sudo apt-get install -y nginx

# Disable firewall
sudo ufw disable
# Create the directory /data/web_static/releases/test and /data/web_static/shared
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a sample html file
echo -e "<html>\n  <head>\n  </head>\n  <body>\n   ALX Software Engineering\n  </body>\n</html>" > /data/web_static/releases/test/index.html

# Create symbolic link between /data/web_static/releases/test/ and /data/web_static/current
sudo ln -sf  /data/web_static/releases/test/ /data/web_static/current

# Give ownership and group of /data to ubuntu
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i '53i\location  /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-available/default

# Restart nginx
sudo service nginx restart
