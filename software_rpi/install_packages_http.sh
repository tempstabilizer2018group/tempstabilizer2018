# run as root!
# Install software for http-server
# The software for the pi  will be installed in another script

# See: http://docs.grafana.org/installation/debian/

apt-get install -y apt-transport-https
echo "deb https://packages.grafana.com/oss/deb stable main" > /etc/apt/sources.list.d/grafana.list
curl https://packages.grafana.com/gpg.key | apt-key add -
apt-get update 
apt-get -y install apache2 apache2-dev libapache2-mod-wsgi-py3 grafana influxdb influxdb-client
update-rc.d grafana-server defaults
systemctl enable grafana-server.service
systemctl unmask influxdb.service
systemctl start influxdb

a2enmod wsgi

# python 3.5
pip3 install PyGithub influxdb mod_wsgi matplotlib markdown

