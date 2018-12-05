apt update
apt upgrade
apt -y autoremove
apt -y install rpi-update grafana influxdb dnsmasq hostapd
rpi-update

apt install python3-pip --reinstall
pip3 install mpfshell esptool influxdb matplotlib markdown

~pi/temp_stabilizer_2018/software_rpi/rpi_root_copyfiles.sh
