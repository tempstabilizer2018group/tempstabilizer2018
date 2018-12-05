apt-get update
apt-get -y upgrade
apt-get -y autoremove
apt-get -y install rpi-update grafana influxdb dnsmasq hostapd
rpi-update

apt install python3-pip --reinstall

pip3 install --upgrade pip
pip3 install PyGithub mpfshell esptool influxdb matplotlib markdown

bash -x ~pi/temp_stabilizer_2018/software_rpi/rpi_root_copyfiles.sh
