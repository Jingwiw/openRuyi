set -eux
test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

baseService sshd.service on
baseService sshd.socket off
baseService NetworkManager.service on
systemctl preset-all
update-ca-trust
