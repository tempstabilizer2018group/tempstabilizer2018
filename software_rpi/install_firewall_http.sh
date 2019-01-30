# run as root!
# Install software for http-server
# The firewall is not installed on the pi

# https://wiki.debian.org/Uncomplicated%20Firewall%20%28ufw%29

apt-get install ufw

ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow http
ufw allow 3000

ufw status verbose

ufw enable

ufw status verbose
