# run as root!
# Install software for the pi
# The software for the http-server  will be installed in another script

apt-get -y install rpi-update picocom dnsmasq hostapd
rpi-update

# python 3.5
pip3 install mpfshell esptool matplotlib

# Disable (Zeroconf/Bonjour/Avahi) Service (UDP Port 5353)
systemctl disable avahi-daemon
systemctl stop avahi-daemon
