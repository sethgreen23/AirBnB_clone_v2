# Puppet script that sets up web servers for the deployment of web_static

  # Update system
  exec { 'apt-update':
    command     => '/usr/bin/apt-get update -y',
    refreshonly => true,
  }

  # Install nginx
  package { 'nginx':
    ensure => installed,
  }

  # Create directories
  file { ['/data/web_static/releases/test', '/data/web_static/shared']:
    ensure => directory,
  }

  # Create sample HTML file
  file { '/data/web_static/releases/test/index.html':
    content => "<html>\n  <head>\n  </head>\n  <body>\n   ALX Software Engineering\n  </body>\n</html>",
  }

  # Create symbolic link
  file { '/data/web_static/current':
    ensure  => link,
    target  => '/data/web_static/releases/test',
    require => File['/data/web_static/releases/test/index.html'],
  }

  # Give ownership and group of /data to ubuntu
  file { '/data':
    ensure  => directory,
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
  }

  # Update nginx configuration
  file { '/etc/nginx/sites-available/default':
    content => template('web_static_setup/nginx_config.erb'),
    notify  => Service['nginx'],
  }

  exec {'update nginx configuration':
  command => "sed -i '60i\location  /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-available/default",
  require =>  Service['nginx'],
  path    => '/bin:/usr/bin',
}
  # Restart nginx
  service { 'nginx':
    ensure    => running,
    enable    => true,
    subscribe => File['/etc/nginx/sites-available/default'],
}
