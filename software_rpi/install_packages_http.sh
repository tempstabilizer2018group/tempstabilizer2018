# run as root!
# Install software for http-server
# The software for the pi  will be installed in another script

apt-get -y install apache2 apache2-dev libapache2-mod-wsgi-py3 grafana influxdb

a2enmod a2enmod wsgi

# python 3.5
pip3 install PyGithub influxdb mod_wsgi matplotlib markdown

