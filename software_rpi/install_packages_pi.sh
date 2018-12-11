# run as root!
# Install software for the pi
# The software for the http-server  will be installed in another script

apt-get update
apt-get -y upgrade
apt-get -y autoremove
apt-get -y install rpi-update dnsmasq hostapd
rpi-update

# python 3.5
apt install python3-pip --reinstall
pip3 install --upgrade pip
pip3 install mpfshell esptool influxdb matplotlib

bash -x ~pi/temp_stabilizer_2018/software_rpi/root_copyfiles_pi.sh
