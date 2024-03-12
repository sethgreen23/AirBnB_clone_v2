#!/usr/bin/env bash
# setup webserver for deployment of web_static

nginx_path=$(command -v nginx)

# install nginx if is not installed
if [ -z "$nginx_path" ]; then
        sudo apt-get update -y
        sudo apt-get install nginx -y
fi
# create the folders if doesnt exist
sudo mkdir -p "/data/web_static/releases/test/"
sudo mkdir -p "/data/web_static/shared/"

# create index.html
sudo echo "
<!doctype html>

<html lang='en'>

  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>HTML Test</title>
  </head>

  <body>
    <h1> Test for deployment </h1>
  </body>

</html>
" | sudo tee "/data/web_static/releases/test/index.html" > /dev/null

# create symblic link to directory
symbolic_link="/data/web_static/current"
source_link="/data/web_static/releases/test/"
if [ -L "$symbolic_link" ]; then
        sudo rm -r  "$symbolic_link"
fi
sudo ln -s  "$source_link" "$symbolic_link"

# ownership of the data folder to ubuntu
sudo chown -hR ubuntu:ubuntu /data/

# update nginx configuration to server content

sudo sed -i '47i\       location /hbnb_static { alias /data/web_static/current/; }' /etc/nginx/sites-enabled/default
#sudo sed -i '55i\      location /hbnb_static {                 alias /data/web_static/current/; }' /etc/nginx/sites-enabled/default
sudo service nginx restart
