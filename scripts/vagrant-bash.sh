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
  
  # Include Django related environment variables
  source docker/django-env.local.vars
  export $(grep -o '^[^ #]*' docker/django-env.local.vars | cut -d= -f1 -)
    
  if [ -f docker/django-env.vars ]
  then
    source docker/django-env.vars
    export $(grep -o '^[^ #]*' docker/django-env.vars | cut -d= -f1 -)
  fi
  
  # Ensure CF plugins are installed
  if which cf >/dev/null
  then
    cf install-plugin -f "/usr/local/bin/cf-autopilot"
    cf install-plugin -f "/usr/local/bin/cf-service-connect"
  fi
fi
