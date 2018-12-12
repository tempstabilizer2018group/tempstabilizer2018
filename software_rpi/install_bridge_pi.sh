# run as root!
# Install the bridge for the pi

brctl addbr br0

brctl addif br0 eth0 wlan0

