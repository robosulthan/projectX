#!/bin/bash
################################################################################
#                              Project Environment setup                       #
#                                                                              #
# Use this template as the beginning of a new program. Place a short           #
# description of the script here.                                              #
#                                                                              #
# Change History                                                               #
# 02/Aug/2023  Aslam Syed    Original code.                                     #
#                                                                              #
#                                                                              #
################################################################################
################################################################################
################################################################################
#                                                                              #
#  Copyright (C) 2023, 2024 Aslam Syed                                         #
#  ikSaan.org                                                                  #
#                                                                              #
#  This program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program; if not, write to the Free Software                 #
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA   #
#                                                                              #
################################################################################
################################################################################
################################################################################

hostname=$(hostname -A)
tmpLog="/tmp/pivpn-install.log"

while [ True ]; do
if [ "$1" = "--install" -o "$1" = "-i" ]; then
    BASE_OPT=1
    shift 1
elif [ "$1" = "--update" -o "$1" = "-r" ]; then
    BASE_OPT=2
    shift 1
elif [ "$1" = "--help" -o "$1" = "-h" ]; then
    BASE_OPT=3
    shift 1
else
    break
fi
done

echo $BASE_OPT
echo $BASE_OPT

###############################################################################################
# Global Environment settings
pEnv() {
        hostname=$(hostname -A)
        IP=`curl -s http://checkip.amazonaws.com`
        user="$USER"
        tmpLog="/tmp/ik-install.log"
        # Update the apt package index:
        sudo apt-get update
        # Install Docker Engine, containerd, and Docker Compose.
        sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        which docker
        if [ $? -eq 0 ]; then
                docker --version | grep "Docker version"
                if [ $? -eq 0 ]; then
                        echo "docker existing"
                else
                        echo "install docker"
                fi
        else
                echo "install docker" >&2
        fi

        sudo usermod -aG docker $user
        sudo apt install -y python3-pip python3-dev nginx
        sudo pip3 install virtualenv
}
###############################################################################################
pUninstall(){
        sudo systemctl stop nginx
        pkill gunicorn
        sudo rm -rf /var/log/gunicorn/
    sudo rm -rf /var/run/gunicorn/
        sudo rm -rf /etc/nginx/sites-enabled/iksaan
        sudo rm -rf /etc/nginx/sites-available/iksaan
        sudo rm -rf /etc/nginx/sites-enabled/default
        sudo rm -rf /etc/nginx/sites-available/default
        sudo rm -rf /var/www/iksaan/static
        #sudo rm -rf /etc/nginx/sites-available/default 2>&1
        #sudo rm -rf /etc/nginx/sites-enabled/default 2>&1
        sudo rm -rf /var/www/iksaan/static 2>&1
}
###############################################################################################
# Gunicorn setup
cGunicornsetup(){
                        sudo mkdir -pv /var/log/gunicorn/
                        sudo mkdir -pv /var/run/gunicorn/
                        sudo chown -cR $user.$user /var/log/gunicorn/
                        sudo chown -cR $user.$user /var/run/gunicorn/
}
###############################################################################################
cNginxsetup(){
        pname=$1
        sudo cp ~/$pname/files/iksaan /etc/nginx/sites-available 2>&1
        sudo ln -s /etc/nginx/sites-available/iksaan /etc/nginx/sites-enabled/ 2>&1
        sudo mkdir -pv /var/www/iksaan/static/ 2>&1
        sudo chown -cR $user.$user /var/www/iksaan 2>&1
        sudo chown -R $user.$user /var/www/iksaan/static 2>&1
}
###############################################################################################
cServices(){
        echo "Restarting nginx service "
        sudo systemctl restart nginx
        Status=$(ps -C nginx >/dev/null && echo "Running" || echo "Not running")
        if [ "$Status" = "Running" ]; then
                echo "site is up and running"
        else
                echo "Manually start nginx service"
        fi
}

###############################################################################################
###############################################################################################
pInstall() {
        echo -n "Project name: "
        read -r pname
        mkdir ~/$pname
        pEnv
        cd ~/$pname
        read
        pwd
        git clone https://github.com/robosulthan/projectX.git ~/$pname && cd "$_" ; echo "cloned" || echo "clone failed"
        DIR=~/$pname/
        echo $DIR
        if [ -d "$DIR" ]; then
                cd $DIR
                virtualenv env
                . $DIR/env/bin/activate
                sed -i 's/ipxxxx/'".iksaan.com\",\"$IP"'/' $DIR/iksaan/settings.py
                pip install -r $DIR/requirements.txt
                echo "export SECRET_KEY='$(openssl rand -hex 40)'" > $DIR/.DJANGO_SECRET_KEY
                . $DIR/.DJANGO_SECRET_KEY
                python manage.py migrate
                if [ -d "/var/log/gunicorn" ]; then
                        pUninstall
                        cGunicornsetup
                else
                        cGunicornsetup
                fi

                if [ -d "/etc/nginx/sites-available/default" ]; then
                        pUninstall
                        cNginxsetup $pname
                        python manage.py collectstatic
                        gunicorn -c $DIR/config/gunicorn/iksaan.py
                else
                        cNginxsetup $pname
                        python manage.py collectstatic
                        gunicorn -c $DIR/config/gunicorn/iksaan.py
                fi
        cServices
        else
                echo "$DIR directory does not exist."
        fi

}

#########################################################################################################


if [ $BASE_OPT = "1" ]; then
   echo "Install"
   pInstall
elif [ $BASE_OPT = "2" ]; then
   echo "Uninstall"
   pUninstall
elif [ $BASE_OPT = "3" ]; then
   echo "Help"
else
   echo "Use --help for more information"
fi


