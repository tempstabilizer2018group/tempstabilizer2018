apt-get update
apt-get -y upgrade
apt-get -y autoremove
apt-get -y install rpi-update apache2 grafana influxdb dnsmasq hostapd libapache2-mod-python
rpi-update

a2enmod python

# python 3.5
apt install python3-pip --reinstall
pip3 install --upgrade pip
pip3 install PyGithub mpfshell esptool influxdb matplotlib markdown

# python 2.7 for apache2
pip install --upgrade pip
python -m pip install PyGithub influxdb

bash -x ~pi/temp_stabilizer_2018/software_rpi/rpi_root_copyfiles.sh
