# run as root!
# Install software for http-server
# The software for the pi  will be installed in another script

apt-get update
apt-get -y upgrade
apt-get -y autoremove
apt-get -y install apache2 libapache2-mod-wsgi-py3 grafana influxdb

a2enmod python

# python 3.5
apt install python3-pip --reinstall
pip3 install --upgrade pip
pip3 install PyGithub influxdb mod_wsgi matplotlib markdown

bash -x ~pi/temp_stabilizer_2018/software_rpi/root_copyfiles_http.sh
