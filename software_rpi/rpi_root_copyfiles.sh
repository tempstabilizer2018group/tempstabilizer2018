# copy all configuration files

cd ~pi/temp_stabilizer_2018/software_rpi/rpi_root

tar cf - . | tar xvf - -C /
