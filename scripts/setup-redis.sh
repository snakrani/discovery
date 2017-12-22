#!/usr/bin/env bash
# Setup local Redis server.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

#set up redis queue
if [ ! -f /etc/init.d/redis ]
then
  #download and install Redis
  cd /tmp
  wget http://download.redis.io/redis-stable.tar.gz
  tar xvzf redis-stable.tar.gz
  
  cd redis-stable
  make
  sudo make install

  #prep operating environment
  sudo mkdir -p /etc/redis
  sudo cp -f redis.conf /etc/redis/6379.conf # binds to 127.0.0.1:6379

  sudo sed -i 's/^daemonize\s.*/daemonize yes/' /etc/redis/6379.conf
  sudo sed -i 's/^dir\s.*/dir "\/var\/redis\/6379"/' /etc/redis/6379.conf
  sudo sed -i 's/^logfile\s.*/logfile "\/var\/log\/redis_6379.log"/' /etc/redis/6379.conf
  sudo sed -i 's/^loglevel\s.*/loglevel debug/' /etc/redis/6379.conf

  sudo mkdir -p /var/redis/6379

  sudo cp -f utils/redis_init_script /etc/init.d/redis # listens at 6379
  sudo update-rc.d redis defaults
fi

#start or restart redis service
sudo /etc/init.d/redis stop
sudo /etc/init.d/redis start
