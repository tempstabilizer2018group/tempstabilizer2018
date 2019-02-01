# Installing Raspberry Pi

- Note: The installing of the HTTP-Server is a subset of the Raspberry Pi (see scripts ending with _http.sh)

## Prepare SDCARD (or USB Stick)

Download
https://downloads.raspberrypi.org/raspbian/images/raspbian-2018-11-15/2018-11-13-raspbian-stretch.zip

Write it to a sdcard using rufus.

## Optional: Boot from USB

https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md

echo program_usb_boot_mode=1 | sudo tee -a /boot/config.txt

## After first Boot
Location: United Kingdom, British English, Timezone London
Check: Use US Keyboard
User pi / raspberry
Set new password: xxx

sudo raspi-config
  4 -> I2, change Timezone: Europe/Zurich
  5 -> P2, SSH: Enable

reboot

-> you may use ssh now

## PREPARATION ONLY HTTP-Server: Set Locale
As root:
dpkg-reconfigure locales
  en_US.UTF-8 UTF-8
echo "LC_ALL=en_US.UTF-8" >> /etc/default/locale
reboot
update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 LANGUAGE
reboot

## PREPARATION ONLY HTTP-Server: User pi
As root:
useradd pi --create-home --shell /bin/bash
adduser pi sudo
passwd pi
xxx
login pi

## PREPARATION
As pi:
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y autoremove

## pip3 is somehow buggy
## These sequences seemed to help
sudo pip3 install --upgrade pip
sudo apt-get install python3-pip --reinstall
sudo pip3 install --upgrade pip

## GIT REPOSITORY
git config --global user.email "hans@maerki.com"
git config --global user.name "Hans Maerki"
git clone https://github.com/tempstabilizer2018group/tempstabilizer2018.git

bash -x ~pi/tempstabilizer2018/software_rpi/install_after_git_clone_http.sh


## INSTALL PACKAGES REQUIRED BY TEMPSTABILIZER
cd ~pi/tempstabilizer2018/software_rpi

sudo bash -x ./install_packages_pi.sh | tee install_packages_pi.log 2>&1
sudo bash -x ./install_packages_http.sh | tee install_packages_http.log 2>&1

sudo bash -x ./root_copyfiles_pi.sh | tee root_copyfiles_pi.log 2>&1
sudo bash -x ./root_copyfiles_http.sh | tee root_copyfiles_http.log 2>&1

## COPY CONFIGURATION FILES
cd ~pi/tempstabilizer2018/software_rpi
sudo bash -x ./install_after_git_clone_http.sh | tee install_after_git_clone_http.log 2>&1

## Reboot to activate access-point
sudo reboot

### Setup fluxdb as in 21_handling_influxdb.md

### Setup grafana as in 21_handling_grafana.md

### Optional: Install Visual Studio Code

See: https://code.headmelted.com/#linux-install-scripts

mkdir visual_studio_code
cd visual_studio_code
sudo -s

## . <( wget -O - https://code.headmelted.com/installers/apt.sh )
bash -x ~pi/tempstabilizer2018/software_rpi/install_visual_studio_code.sh
