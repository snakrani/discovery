#!/usr/bin/env bash
# Setup local Redis server.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

#set up redis queue
if [ ! -f /etc/init.d/redis ]
then
  #download and install Redis
  echo "> Downloading and installing Redis"
  cd /tmp
  wget --quiet http://download.redis.io/redis-stable.tar.gz
  tar -xzf redis-stable.tar.gz
  
  cd redis-stable
  make > /dev/null 2>&1
  sudo make install > /dev/null 2>&1

  #prep operating environment
  echo "> Modifying Redis configurations"
  sudo mkdir -p /etc/redis
  sudo cp -f redis.conf /etc/redis/6379.conf # binds to 127.0.0.1:6379 by default

  sudo sed -i 's/^bind\s.*/bind 0.0.0.0/' /etc/redis/6379.conf # allow remote connections
  sudo sed -i 's/^daemonize\s.*/daemonize yes/' /etc/redis/6379.conf
  sudo sed -i 's/^dir\s.*/dir "\/var\/redis\/6379"/' /etc/redis/6379.conf
  sudo sed -i 's/^logfile\s.*/logfile "\/var\/log\/redis_6379.log"/' /etc/redis/6379.conf
  sudo sed -i 's/^loglevel\s.*/loglevel debug/' /etc/redis/6379.conf

  sudo mkdir -p /var/redis/6379

  echo "> Copying Redis service configurations and scripts"
  sudo cp -f utils/redis_init_script /etc/init.d/redis # listens at 6379
  sudo update-rc.d redis defaults > /dev/null 2>&1
fi

#start or restart redis service
echo "> Starting the Redis queue"
sudo /etc/init.d/redis stop > /dev/null
sudo /etc/init.d/redis start > /dev/null
