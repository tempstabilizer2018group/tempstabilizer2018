# run as root!
# copy all configuration files

ROOT=~pi/tempstabilizer2018/software_rpi/root_http
cd $ROOT

systemctl stop apache2

issymlink() {
    test "$(readlink "${1}")";
}

# Copy files to /
# tar cf - . | tar xvf - -C /

# Create symbolic links
# If a file 'xy.txt' exists, rename it to 'xy.txt.bak'.
for f in $(find * -type f)
do
  echo ln -s $ROOT/$f /$f
  if issymlink /$f; then
    rm /$f
  else
    echo Make backup
    mv /$f /${f}.bak
  fi
  ln -s $ROOT/$f /$f
done

systemctl start apache2
