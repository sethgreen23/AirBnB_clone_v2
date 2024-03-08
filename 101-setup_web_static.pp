# Puppet script to setup web_static delivery for servers

# Update system
exec { 'apt-update':
  command => '/usr/bin/apt-get update -y',
}

# Install nginx
package { 'nginx':
  ensure => installed,
}

# Disable firewall
exec { 'disable-ufw':
  command => '/usr/sbin/ufw disable',
}

# Create the directory /data/web_static/releases/test and /data/web_static/shared
file { '/data/web_static/releases/test':
  ensure => directory,
}

file { '/data/web_static/shared':
  ensure => directory,
}

# Create a sample html file
file { '/data/web_static/releases/test/index.html':
  content => "<html>\n  <head>\n  </head>\n  <body>\n   ALX Software Engineering\n  </body>\n</html>",
}

# Create symbolic link between /data/web_static/releases/test/ and /data/web_static/current
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  force  => true,
}

# Give ownership and group of /data to ubuntu
exec { 'chown-data-directory':
  command => '/bin/chown -R ubuntu:ubuntu /data/',
}

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
exec { 'update-nginx-config':
  command => '/bin/bash -c "echo \'location  /hbnb_static { alias /data/web_static/current/;}\' >> /etc/nginx/sites-available/default"',
  require => File['/etc/nginx/sites-available/default'],
}

# Restart nginx
exec { 'restart-nginx':
  command => '/usr/sbin/service nginx restart',
  require => Exec['update-nginx-config'],
}
