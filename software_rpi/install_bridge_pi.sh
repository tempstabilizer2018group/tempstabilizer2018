# run as root!
# Install software for the pi
# The software for the http-server  will be installed in another script

apt-get -y install rpi-update dnsmasq hostapd bridge-utils
rpi-update

# python 3.5
pip3 install mpfshell esptool matplotlib

