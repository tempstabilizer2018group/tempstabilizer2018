https://github.com/micropython/micropython/commit/a90124a9e20fac828aa6e7702f8196092ee354b0#diff-f91c90ad9d63483d6172b47a84109147


Anleitung
=========
https://github.com/micropython/micropython/tree/master/ports/esp32


sudo apt-get install gcc git wget make libncurses-dev flex bison gperf python python-serial

wget https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
tar -xzf xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz


git clone https://github.com/micropython/micropython.git
cd micropython
git submodule update --init

git clone https://github.com/micropython/micropython-lib.git
cd micropython-lib
git checkout 1.9.3

git clone https://github.com/espressif/esp-idf.git
grep ESPIDF_SUPHASH micropython/ports/esp32/Makefile
  -> 30545f4cccec7460634b656d278782dd7151098e
git checkout 30545f4cccec7460634b656d278782dd7151098e
git submodule update --init --recursive


export PATH="$PATH:$HOME/micropython/esp32/xtensa-esp32-elf/bin"

alias get_esp32='export PATH="$PATH:$HOME/micropython/esp32/xtensa-esp32-elf/bin"'
export ESPIDF=~/micropython/esp32/esp-idf

BUILD
-----
cd ~/micropython/esp32/micropython
make -C mpy-cross
cd ports/esp32
make CONFIG_SPIRAM_SUPPORT=0

-> build/firmware.bin

FLASH
-----
make erase
make deploy

picocom -b 115200 /dev/ttyUSB0
