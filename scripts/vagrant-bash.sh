#
# This script is concatenated to the end of the Vagrant user .bashrc file during 
# provisioning if it has not been already.  This process checks for the presence
# of a <<discovery>> comment so do not remove it unless you want the Vagrant
# provisioner to append it again.
#
#<<discovery>>

# Setup Git prompt (if used)
if [ ! -f ~/.git-prompt.sh ]
then
  wget -q -O ~/.git-prompt.sh https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
fi
source ~/.git-prompt.sh

# Change directory to the project directory if it exists
if [ -d /vagrant ]
then
  cd /vagrant
  
  # Refresh Docker Compose cluster
  if which docker-compose >/dev/null
  then
    docker-compose up -d
  fi
fi

# Activate Python virtual environment if present
if [ -d /venv ]
then
  source /venv/bin/activate
fi
