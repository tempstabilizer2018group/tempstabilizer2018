# run as root!

# copy all configuration files

systemctl stop dnsmasq
systemctl stop hostapd

cd ~pi/temp_stabilizer_2018/software_rpi/rpi_root

tar cf - . | tar xvf - -C /

systemctl start dnsmasq
systemctl start hostapd
