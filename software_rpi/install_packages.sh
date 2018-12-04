apt update
apt upgrade
apt -y autoremvoe
apt -y install rpi-update grafana influxdb dnsmasq hostapd
rpi-update

apt install python3-pip --reinstall
pip3 install mpfshell esptool influxdb matplotlib markdown

# copy all configuration files
cp -r ~pi/temp_stabilizer_2018/software_rpi/rpi_root /
